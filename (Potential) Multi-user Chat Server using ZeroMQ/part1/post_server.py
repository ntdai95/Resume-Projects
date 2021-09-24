import zmq
import argparse


class ServerData:
    message_server_memory = []

    def add_message(cls, message):
        cls.message_server_memory.append(message)

parser = argparse.ArgumentParser(prog = "server", description = "Server")
parser.add_argument("ip", help = "Please, enter the ip address for the server.")
parser.add_argument("post_port", help = "Please, enter the server's posting port number between 1024 and 65535.")
args = parser.parse_args()

if args.post_port.isnumeric() and 1024 <= int(args.post_port) <= 65535:
    context = zmq.Context()
    post_socket = context.socket(zmq.REP)
    post_socket.bind(f"tcp://{args.ip}:{args.post_port}")

    while True:
        message = post_socket.recv_string()
        print(message)
        ServerData().add_message(message)
        post_socket.send_string("Message arrived to the server.")
else:
    print("Please, enter a valid server posting port number (between 1024 and 65535, inclusive).")