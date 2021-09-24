import socket
import random
import time
import struct
import threading
import argparse


class PingClient:


    def __init__(self):
        """Using argparse to parse out the user input arguments and if all the arguments are valid, then run the main program of
        ping_client_run() below."""

        self.parser = argparse.ArgumentParser(prog = "ping_client", description = "Ping Protocol Client")
        self.parser.add_argument("server_ip", help = "Please, enter the server ip.")
        self.parser.add_argument("server_port", help = "Please, enter the server port number between 1024 and 65535.")
        self.parser.add_argument("count", help = "Please, enter the number of ping requests to send to the ping server.")
        self.parser.add_argument("period", help = "Please, enter the amount of time in milliseconds to wait between sending each ping request.")
        self.parser.add_argument("timeout", help = "Please, enter the amount of time in milliseconds to wait for a reply for each ping request.")
        self.args = self.parser.parse_args()
        self.server_ip, self.server_port, self.count, self.period, self.timeout = self.user_input_parsing_and_checking()
        if self.server_ip != None:
            # since we are using the process id for the identifier, we don't want it to go over 65535
            self.process_identifier = random.randint(1, 65535)
            self.process_identifier_in_bytes = self.process_identifier.to_bytes(2, "big")
            self.number_of_received_packets = 0
            self.number_of_transmitted_requests = 0
            self.start_time = 0
            self.list_of_times = []
            self.ping_client_run()
    

    def user_input_parsing_and_checking(self):
        """Checking the user input validity: server_port - integer between 1024 and 65535 inclusive, count - integer greater than 0,
        period - float greater than 0, and timeout - float greater than 0"""

        wrong_input = False
        server_ip = self.args.server_ip

        if self.args.server_port.isnumeric() and 1024 <= int(self.args.server_port) <= 65535:
            server_port = int(self.args.server_port)
        else:
            print("Please, enter a valid server port number between 1024 and 65535, inclusive.")
            wrong_input = True
        if self.args.count.isnumeric() and int(self.args.count) > 0:
            count = int(self.args.count)
        else:
            print("Please, enter a valid number (integer greater than 0) of ping requests to send to the ping server.")
            wrong_input = True
        try:
            period = float(self.args.period)
            if period < 0:
                raise ValueError
        except ValueError:
            print("Please, enter a valid amount of time in milliseconds to wait between sending each ping request.")
            wrong_input = True
        try:
            timeout = float(self.args.timeout)
            if timeout < 0:
                raise ValueError
        except ValueError:
            print("Please, enter a valid amount of time in milliseconds to wait for a reply for each ping request.")
            wrong_input = True

        if wrong_input:
            return None, None, None, None, None
        else:
            return server_ip, server_port, count, period, timeout


    def internet_checksum_calculating(self, data):
        """Unpacking the checksum values from the message and calculating the ones' complement of the ones' complement sum. If the 
        resut is greater than 2**16 then wrap 1 around"""

        values_to_checksum = struct.unpack("!%dH" % (len(data) / 2), data)
        checksum = 0
        for value in values_to_checksum:
            checksum += value
            # carrying around the 1 if the resulting checksum is greater than 2**16
            if checksum > 2**16:
                checksum = (checksum & 0xFFFF) + 1
        return checksum


    def statistics(self):
        """Creating and printing out the resulting statistics after the last request sent and the last reply received/or not for the
        user"""

        loss_percentage = int(100 - ((self.number_of_received_packets / self.number_of_transmitted_requests) * 100))
        total_elapsed_time = int((time.time() - self.start_time) * 1000)
        print(f"\n--- {self.server_ip} ping statistics ---\n{self.number_of_transmitted_requests} transmitted, {self.number_of_received_packets} received, {loss_percentage}% loss, time {total_elapsed_time} ms")

        if len(self.list_of_times) == 0:
            print("rrt min/avg/max == 0/0/0 ms")
        else:
            minimum_time = min(self.list_of_times)
            average_time = int(sum(self.list_of_times) / len(self.list_of_times))
            maximum_time = max(self.list_of_times)
            print(f"rrt min/avg/max == {minimum_time}/{average_time}/{maximum_time} ms")


    def ping_client_request_sending(self, seqno, timestamp):
        """Creating client data packet for ping request to send to the server as asked on the page 2 of the project 3.pdf file with 
        network byte order (big endian)"""

        seqno_in_bytes = seqno.to_bytes(2, "big")
        timestamp_in_bytes = int(timestamp * 1000).to_bytes(6, "big")
        checksum = 0
        checksum_in_bytes = checksum.to_bytes(2, "big")
        client_checksum_packet = bytearray()
        client_checksum_packet.insert(0, 8)
        client_checksum_packet.insert(1, 0)
        client_checksum_packet.extend(checksum_in_bytes)
        client_checksum_packet.extend(self.process_identifier_in_bytes)
        client_checksum_packet.extend(seqno_in_bytes)
        client_checksum_packet.extend(timestamp_in_bytes)

        checksum = 0xFFFF - self.internet_checksum_calculating(client_checksum_packet)
        checksum_in_bytes = checksum.to_bytes(2, "big")
        client_data_packet = bytearray()
        client_data_packet.insert(0, 8)
        client_data_packet.insert(1, 0)
        client_data_packet.extend(checksum_in_bytes)
        client_data_packet.extend(self.process_identifier_in_bytes)
        client_data_packet.extend(seqno_in_bytes)
        client_data_packet.extend(timestamp_in_bytes)
        return client_data_packet


    def ping_server_reply_receiving(self, timestamp, ping_client_UDP_socket):
        """Receiving ping server reply, check the checksum of it, and if it's correct calculate the elapsed time between the sent request
        and the arrived reply, else printing out the failed meassage with the request's seqno."""

        ping_server_data, ping_server_address = ping_client_UDP_socket.recvfrom(2048)
        end_time = time.time()
        ping_server_checksum = self.internet_checksum_calculating(ping_server_data)
        ping_server_seqno = int.from_bytes(ping_server_data[6:8], "big")

        # Note that for correct checksum, all of the 16-bits must be ones, which would be 2**16 - 1 = 65535
        if ping_server_checksum != 65535:
            print(f"Checksum verification failed for echo reply seqno={ping_server_seqno}")
        else:
            elapsed_time = int((end_time - timestamp) * 1000)
            ping_server_ip = ping_server_address[0]
            self.list_of_times.append(elapsed_time)
            self.number_of_received_packets += 1
            print(f"PONG {ping_server_ip}: seq={ping_server_seqno} time={elapsed_time}")


    def ping_request_and_reply_handling(self, seqno):
        """Creating a socket for a ping request and listening for ping replies. If timeout occurs between the request and reply, then
        update the appropriate statistics and move to close the socket."""

        ping_client_UDP_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ping_client_UDP_socket.settimeout(self.timeout / 1000)
        timestamp = time.time()
        # For the first request, start the time and print out the server_ip for the user
        if seqno == 1:
            self.start_time = timestamp
            print(f"PING {self.server_ip}")

        try:
            client_data_packet = self.ping_client_request_sending(seqno, timestamp)
            ping_client_UDP_socket.sendto(client_data_packet, (self.server_ip, self.server_port))
            self.ping_server_reply_receiving(timestamp, ping_client_UDP_socket)
        # If timeout happens, then don't do anything and move to update the statistics and close the socket          
        except OSError:
            pass
        finally:
            self.number_of_transmitted_requests += 1
            ping_client_UDP_socket.close()
            if self.number_of_transmitted_requests == self.count:
                self.statistics()
            return


    def ping_client_run(self):
        """Using threading, the client creates a ping request in a new thread and update the seqno after each user entered period time.
        Note that it does not discard any dead thread to print out the statistics at the end."""

        seqno = 1
        list_of_threads = []
        for i in range(self.count):
            t = threading.Timer(self.period * i / 1000, self.ping_request_and_reply_handling, args = [seqno])
            seqno += 1
            t.start()
            list_of_threads.append(t)

        for thread in list_of_threads:
            thread.join()


if __name__ == "__main__":
    PingClient()