from socket import *
from threading import *
from argparse import *
import random
import datetime


class TFTPServer:
    def __init__(self):
        # Initializing opcodes, error messages, and data block size
        self.rrq_opcode = 1
        self.wrq_opcode = 2
        self.data_opcode = 3
        self.ack_opcode = 4
        self.error_opcode = 5
        self.error_messages = {0: "Not defined, see error message (if any).",
                               1: "File not found.",
                               2: "Access violation",
                               3: "Disk full or allocation exceeded.",
                               4: "Illegal TFTP operation.",
                               5: "Unknown transfer ID.",
                               6: "File already exists.",
                               7: "No such user."}
        self.data_size = 512

        # Parsing out the port number and timeout value from the user entered command line
        self.parser = ArgumentParser(prog = "tftp_server", description = "Trivial File Transfer Protocol (TFTP)")
        self.parser.add_argument("port", help = "Please, enter a port number.")
        self.parser.add_argument("timeout", help = "Please, enter a timeout in milliseconds.")
        self.args = self.parser.parse_args()
        # Checking the user input
        try:
            self.timeout = float(self.args.timeout)
            self.port = int(self.args.port)
            if self.port < 1024 or self.port > 65535:
                raise ValueError
            # Creating and binding socket
            self.hostname = gethostname()
            self.server_socket = socket(AF_INET, SOCK_DGRAM)
            self.server_socket.bind((self.hostname, self.port))
        except ValueError:
            print("Please, enter server port number as an integer between 1024 and "
                  "65535, inclusive and timeout value as a floating point integer.")

    
    def run(self):
        # Using threading to allow multiple sockets to be accepted and data to be transferred from multiple clients
        list_of_threads = []
        while True:
            # header of 2 bytes + block number of 2 bytes + data is a size of 512 bytes = 516 bytes
            client_data, client_address = self.server_socket.recvfrom(2 + 2 + self.data_size)
            opcode = client_data[1]
            # Checking the opcodes and start the thread with the corresponding function
            if opcode == self.rrq_opcode:
                t = Thread(target = self.receiving_read_request(), args = [client_address, client_data])
                t.start()
                list_of_threads.append(t)
            elif opcode == self.wrq_opcode:
                t = Thread(target = self.receiving_write_request(), args = [client_address, client_data])
                t.start()
                list_of_threads.append(t)
            # Joining those threads in the list which are still alive and discarding the others
            for index, thread in enumerate(list_of_threads):
                if thread.is_alive():
                    thread.join()
                else:
                    del list_of_threads[index]
            # Closing down the socket after accepted from the client
            self.server_socket.close()

    
    def receiving_read_request(self, client_address, client_data):
        # Creating the ephemeral socket and port between the server and the client from whom the server received the read request
        ephemeral_socket = socket(AF_INET, SOCK_DGRAM)
        ephemeral_port = random.randint(1024, 65535)
        ephemeral_hostname = gethostname()
        ephemeral_socket.bind((ephemeral_hostname, ephemeral_port))
        # Using the asked filename from the client, the server is breaking down the file 
        # to be sent into chunks of data size of 512 bytes
        client_filename = client_data[2:]
        byte_parts = []
        with open(client_filename, "rb") as f:
            byte = f.read(self.data_size)
            while byte != b"":
                byte_parts.append(byte)
                byte = f.read(self.data_size)
        # Creating and sending out the first data packet
        first_data_part = byte_parts[0]
        data_packet = bytearray()
        data_packet.insert(0, 0)
        data_packet.insert(1, self.data_opcode)
        data_packet.insert(2, 0)
        data_packet.insert(3, 1)
        data_packet[4:4] = first_data_part
        ephemeral_socket.sendto(data_packet, client_address)
        # Retrieving the opcode from the client sent data and set ack block number to be 
        # 1 because we just sent out the first data packet above
        opcode = client_data[1]
        ack_block_number = 1
        counts_of_received_ack_numbers = []
        # Creating a while loop to keep listening and accepting data from the client until 
        # all of the data has been sent out or there was an error
        while True:
            timeout = datetime.now() + datetime.timedelta(milliseconds = self.timeout)
            while datetime.now() < timeout:
                client_data, client_address = ephemeral_socket.recvfrom(self.data_size + 2 + 2)
                opcode = client_data[1]

                if opcode == self.ack_opcode:
                    received_ack_number = client_data[3]
                    # if the received block number is the same as the lenght of the data parts to 
                    # be sent out, then we have sent out all of the data packets
                    if received_ack_number == len(byte_parts):
                        print("All data packets have been sent.")
                        ephemeral_socket.close()
                        return
                    # if we received a block number which is previously not in the list of received 
                    # block numbers, then the client has received the data packet that we just sent, 
                    # so sending the next one
                    elif received_ack_number not in counts_of_received_ack_numbers:
                        counts_of_received_ack_numbers.append(received_ack_number)
                        if received_ack_number < len(byte_parts):
                            if received_ack_number == ack_block_number:
                                ack_block_number += 1
                                data_packet = bytearray()
                                data_packet.insert(0, 0)
                                data_packet.insert(1, self.data_opcode)
                                data_packet.insert(2, 0)
                                data_packet.insert(3, ack_block_number)
                                # Note that we already sent out the first part of data and we should 
                                # expect 1 to come back as a received ack block number, so sending the 
                                # second part of the data at index 1, using the value of received 
                                # ack block number
                                data_packet[4:4] = byte_parts[received_ack_number]
                                ephemeral_socket.sendto(data_packet, client_address)
                    # if we received a duplicate ack, then just keep listening for the new ack
                # If the we get the error packet, then print out the corresponding error message, and then close the socket
                elif opcode == self.error_opcode:
                    error_code = client_data[3]
                    error_msg = self.error_messages[error_code]
                    print(f"Error code {error_code}: {error_msg}")
                    ephemeral_socket.close()
                    return
            # if there is a timeout, and did not get any response, then we just sent the last data packet to the client again
            ephemeral_socket.sendto(data_packet, client_address)


    def receiving_write_request(self, client_address, client_data):
        # Creating the ephemeral socket and port between the server and the client from whom the server received the write request
        ephemeral_socket = socket(AF_INET, SOCK_DGRAM)
        ephemeral_port = random.randint(1024, 65535)
        ephemeral_hostname = gethostname()
        ephemeral_socket.bind((ephemeral_hostname, ephemeral_port))
        # sending out the 0th ack packet to client
        ack_packet = bytearray()
        ack_packet.insert(0, 0)
        ack_packet.insert(1, self.ack_opcode)
        ack_packet.insert(2, 0)
        ack_packet.insert(3, 0)
        ephemeral_socket.sendto(ack_packet, client_address)
        # Opening up the file based on the filename that we received from the client
        client_filename = client_data[2:]
        f = open(f"{client_filename}", "wb")
        # Retrieving the opcode from the client sent data and set data block number 
        # to be 1 because we are expecting to get the first data packet from the client
        opcode = client_data[1]
        data_block_number = 1
        counts_of_received_data_numbers = []
        # Creating a while loop to keep listening and accepting data from the client 
        # until all of the data has been received or there was an error
        while True:
            timeout = datetime.now() + datetime.timedelta(milliseconds = self.timeout)
            while datetime.now() < timeout:
                client_data, client_address = ephemeral_socket.recvfrom(self.data_size + 2 + 2)
                opcode = client_data[1]

                if opcode == self.data_opcode:
                    received_data_number = client_data[3]
                    if received_data_number == data_block_number and received_data_number not in counts_of_received_data_numbers:
                        # If the last data packet has a smaller size than the block size, it 
                        # means that we are receiving the last part of the data, so we are 
                        # done after written out to the file above.
                        if len(client_data) < self.data_size:
                            f.close()
                            print("All data packets have been received.")
                            return
                        else:
                            received_data = client_data[4:]
                            f.write(received_data)
                            data_block_number += 1
                            ack_packet = bytearray()
                            ack_packet.insert(0, 0)
                            ack_packet.insert(1, self.ack_opcode)
                            ack_packet.insert(2, 0)
                            ack_packet.insert(3, received_data_number)
                            ephemeral_socket.sendto(ack_packet, client_address)
                            counts_of_received_data_numbers.append(received_data_number)
                    # if we received a duplicate data block number or the expected and received data block numbers 
                    # do not match, then that means the client did not received our previous ack packet, so send it again        
                    else:
                        ack_packet = bytearray()
                        ack_packet.insert(0, 0)
                        ack_packet.insert(1, self.ack_opcode)
                        ack_packet.insert(2, 0)
                        ack_packet.insert(3, received_data_number)
                        ephemeral_socket.sendto(ack_packet, client_address)
                # If the we get the error packet, then print out the corresponding error message, and then close the socket
                elif opcode == self.error_opcode:
                    error_code = client_data[3]
                    error_msg = self.error_messages[error_code]
                    print(f"Error code {error_code}: {error_msg}")
                    ephemeral_socket.close()
                    return
            # if there is a timeout, and did not get any response, then we just sent the last ack packet to the client again
            ephemeral_socket.sendto(ack_packet, client_address)


if __name__ == "__main__":
    TFTPServer().run()
