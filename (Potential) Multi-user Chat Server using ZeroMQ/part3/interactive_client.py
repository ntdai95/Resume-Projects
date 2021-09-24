import zmq
from datetime import datetime
import sys
import argparse
import threading


parser = argparse.ArgumentParser(prog = "client", description = "client")
parser.add_argument("ip", help = "Please, enter the ip address for the server.")
parser.add_argument("post_port", help = "Please, enter the server's posting port number between 1024 and 65535.")
parser.add_argument("pub_port", help = "Please, enter the server's publishing port number between 1024 and 65535.")
parser.add_argument("name", help = "Please, enter your username.")
args = parser.parse_args()

def posting_channel(args_ip, args_post_port, args_name, context):
    while True:
        message = input()
        if message:
            post_socket = context.socket(zmq.REQ)
            post_socket.connect(f"tcp://{args_ip}:{args_post_port}")
            now = datetime.now()
            current_time = now.strftime("%m/%d/%Y %H:%M:%S")
            post_message = f"{args_name},{current_time},{message}"
            post_socket.send_string(post_message)
            post_socket.recv_string()
            post_socket.close()

def publishing_channel(args_ip, args_pub_port, context):
    while True:
        pub_socket = context.socket(zmq.SUB)
        pub_socket.connect(f"tcp://{args_ip}:{args_pub_port}")
        pub_socket.subscribe("")
        pub_message = pub_socket.recv_string()
        sys.stdout.write(pub_message + "\n")

if args.post_port.isnumeric() and 1024 <= int(args.post_port) <= 65535 and args.pub_port.isnumeric() and 1024 <= int(args.pub_port) <= 65535:
    context = zmq.Context()
    post_thread = threading.Thread(target = posting_channel, args = [args.ip, args.post_port, args.name, context])
    pub_thread = threading.Thread(target = publishing_channel, args = [args.ip, args.pub_port, context])
    post_thread.start()
    pub_thread.start()
    post_thread.join()
    pub_thread.join()

elif args.post_port.isnumeric() and 1024 <= int(args.post_port) <= 65535:
    print("Please, enter a valid server publishing port number (between 1024 and 65535, inclusive).")
elif args.pub_port.isnumeric() and 1024 <= int(args.pub_port) <= 65535:
    print("Please, enter a valid server posting port number (between 1024 and 65535, inclusive).")
else:
    print("Please, enter valid server posting and publishing port numbers (between 1024 and 65535, inclusive).")