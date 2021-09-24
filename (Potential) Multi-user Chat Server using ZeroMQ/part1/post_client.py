import zmq
from datetime import datetime
import argparse


parser = argparse.ArgumentParser(prog = "client", description = "client")
parser.add_argument("ip", help = "Please, enter the ip address for the server.")
parser.add_argument("post_port", help = "Please, enter the server's posting port number between 1024 and 65535.")
parser.add_argument("username", help = "Please, enter your username.")
parser.add_argument("message", help = "Please, enter a message that you wish to post to the server.")
args = parser.parse_args()

if args.post_port.isnumeric() and 1024 <= int(args.post_port) <= 65535:
    now = datetime.now()
    current_time = now.strftime("%m/%d/%Y %H:%M:%S")
    message = f"{args.username},{current_time},{args.message}"

    context = zmq.Context()
    post_socket = context.socket(zmq.REQ)
    post_socket.connect(f"tcp://{args.ip}:{args.post_port}")
    post_socket.send_string(message)
    print(post_socket.recv_string())
else:
    print("Please, enter a valid server posting port number (between 1024 and 65535, inclusive).")