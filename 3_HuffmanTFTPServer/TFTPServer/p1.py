import socket
import sys
import errno
import struct
import time
from threading import Thread

# UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# input check
try:
    PORT = int(sys.argv[1])
    TIMEOUT = int(sys.argv[2]) / 1000
except IndexError:
    sys.exit("Please make sure you have two inputs.")
except ValueError:
    sys.exit("Please make sure both inputs are integers.")    
if PORT < 1024:
    sys.exit("Please use a port between 1024 and 65535.")
# connection check
HOST = '0.0.0.0'
try:
    s.bind((HOST, PORT))
except OSError as e:
    if e.errno == errno.EADDRINUSE:
        sys.exit("This port is already in use. Try another one.")
    else:
        sys.exit("Unexpected error: {0}".format(e))
print("Connected.")

# TFTP parameters
MODE = 'octet'  # not used; mode is hardcoded
RRQ, WRQ, DATA, ACK, ERROR = range(1,6)
ERR_MSG = [
    "Not defined, see error message (if any).", # 0
    "File not found.",                          # 1
    "Access violation.",                        # 2
    "Disk full or allocation exceeded.",        # 3
    "Illegal TFTP operation.",                  # 4
    "Unknown transfer ID.",                     # 5
    "File already exists.",                     # 6
    "No such user."                             # 7
]
MAX_DATA = 512  # length of data, header not included

requests = []  # RRQ, WRQ only
request_packets = {}  # key: addr, value: DATA or ACK packets

def unpack_request_packet(request_packet):
    """
    2 bytes    string   1 byte   string   1 byte
    --------------------------------------------
    | Opcode | Filename |   0   |  Mode  |   0  |
    --------------------------------------------
    """
    filename = request_packet[2:-7].decode('ascii')
    return filename

def pack_data_packet(data_block_num, data):
    """
    2 bytes     2 bytes      n bytes
    ----------------------------------
    | Opcode |   Block #  |   Data    |
    ----------------------------------
    """
    return struct.pack('!HH', DATA, data_block_num) + data.encode("ascii")

def unpack_data_packet(data_packet):
    data_block_num = struct.unpack('!H', data_packet[2:4])[0]
    data = data_packet[4:].decode('ascii')
    return data_block_num, data

def pack_ack_packet(ack_block_num):
    """
     2 bytes     2 bytes
    ---------------------
    | Opcode |  Block #  |
    ---------------------
    """
    return struct.pack('!HH', ACK, ack_block_num)

def unpack_ack_packet(ack_packet):
    ack_block_num = struct.unpack('!H', ack_packet[2:4])[0]
    return ack_block_num

def pack_error_packet(err_code):
    """
    2 bytes     2 bytes      string    1 byte
    -----------------------------------------
    | Opcode |  ErrorCode |  ErrMsg   |   0  |
    -----------------------------------------
    """
    msg = ERR_MSG[err_code].encode('ascii');
    format = '!HH{}sB'.format(len(msg))
    return struct.pack(format, ERROR, err_code, msg, 0)

def unpack_error_packet(error_packet):
    err_code = struct.unpack('!H', error_packet[2:4])[0]
    msg = error_packet[4:-1].decode('ascii')
    return "TFTP error {}: {}".format(err_code, msg)

def get_opcode(packet):
    return int(struct.unpack('!H', packet[:2])[0])

def get_blocknum(packet):
    return int(struct.unpack('!H', packet[2:4])[0])

def read(filename, addr):
    global requests, request_packets
    try:
        f = open(filename, 'r')
    except:
        s.sendto(pack_error_packet(1), addr)
        return
    
    print("Reading file {} from {} ...".format(filename, addr))
    data_num = 0
    acked = True
    while True:
        if acked == True:
            data = f.read(MAX_DATA)
            data_num += 1
            attempt = 0
        while len(request_packets[addr]) == 0:
            s.sendto(pack_data_packet(data_num, data), addr)
            acked = False
            attempt += 1
            print("Data {} ({} bytes) sent to {} (attemp {})."
                    .format(data_num, len(data), addr, attempt))
            time.sleep(TIMEOUT)
        while len(request_packets[addr]) > 0:
            opcode, packet = request_packets[addr].pop(0)
            if (opcode == ACK):
                ack_num = unpack_ack_packet(packet)
                if (ack_num == data_num):
                    print("Ack {} from {} received.".format(ack_num, addr))
                    acked = True
                    request_packets[addr] = []
        if (len(data) < MAX_DATA) and (acked == True):
            f.close()
            print("Finish reading {} from {}.".format(filename, addr))
            request_packets.pop(addr)
            break

def write(filename, addr):
    global requests, request_packets
    try:
        f = open(filename, 'x')
    except:
        s.sendto(pack_error_packet(6), addr)
        return
    
    f.close()
    f = open(filename, 'a')
    print("Writing file {} from {} ...".format(filename, addr))
    data_received = True
    attempt = 0
    ack_num = 0
    while True:
        while len(request_packets[addr]) == 0:
            s.sendto(pack_ack_packet(ack_num), addr)
            attempt += 1
            print("Ack {} sent to {} (attemp {})."
                    .format(ack_num, addr, attempt))
            time.sleep(TIMEOUT)
        while len(request_packets[addr]) > 0:
            opcode, packet = request_packets[addr].pop(0)
            if (opcode == DATA):
                data_num, data = unpack_data_packet(packet)
                if data_num == ack_num + 1:
                    print("Data {} ({} bytes) from {} received."
                            .format(data_num, len(data), addr))
                    data_received = True
                    f.write(data)
                    request_packets[addr] = []
                    ack_num += 1
                    attempt = 0
        if (len(data) < MAX_DATA) and (data_received == True):
            s.sendto(pack_ack_packet(ack_num), addr)
            f.close()
            print("Finish writing {} from {}.".format(filename, addr))
            request_packets.pop(addr)
            break
        

def listen_packets():
    global requests, request_packets
    print("Start listening...")
    while True:
        packet, addr = s.recvfrom(1024)
        opcode = get_opcode(packet)
        if (opcode in (RRQ, WRQ)):
            filename = unpack_request_packet(packet)
            requests.append((opcode, filename, addr))
        elif (opcode in (DATA, ACK)):
            if request_packets.get(addr) != None:

                request_packets[addr].append((opcode, packet))
        else:
            sys.exit(unpack_error_packet(packet))
    

def main():
    packet_listening_thread = Thread(target=listen_packets)
    packet_listening_thread.start()
    while True:
        if (len(requests) > 0):
            opcode, filename, addr = requests.pop(0)
            request_packets[addr] = []
            if (opcode == RRQ):
                t = Thread(target=read, args=(filename, addr))
            else:
                t = Thread(target=write, args=(filename, addr))
            t.start()
    

if __name__ == "__main__":
    main()