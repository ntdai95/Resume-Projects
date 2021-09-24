import zmq
import argparse


parser = argparse.ArgumentParser(prog = "client", description = "client")
parser.add_argument("ip", help = "Please, enter the ip address for the server.")
parser.add_argument("pub_port", help = "Please, enter the server's publishing port number between 1024 and 65535.")
args = parser.parse_args()

if args.pub_port.isnumeric() and 1024 <= int(args.pub_port) <= 65535:
    context = zmq.Context()
    pub_socket = context.socket(zmq.SUB)
    pub_socket.connect(f"tcp://{args.ip}:{args.pub_port}")
    pub_socket.subscribe("")
    
    while True:
        pub_message = pub_socket.recv_string()
        print(pub_message)
else:
    print("Please, enter a valid server publishing port number (between 1024 and 65535, inclusive).")