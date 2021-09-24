import zmq
import argparse


class ServerData:
    message_server_memory = []

    def add_message(cls, message):
        cls.message_server_memory.append(message)

parser = argparse.ArgumentParser(prog = "server", description = "Server")
parser.add_argument("ip", help = "Please, enter the ip address for the server.")
parser.add_argument("post_port", help = "Please, enter the server's posting port number between 1024 and 65535.")
parser.add_argument("pub_port", help = "Please, enter the server's publishing port number between 1024 and 65535.")
args = parser.parse_args()

if args.post_port.isnumeric() and 1024 <= int(args.post_port) <= 65535 and args.pub_port.isnumeric() and 1024 <= int(args.pub_port) <= 65535:
    context = zmq.Context()
    post_socket = context.socket(zmq.REP)
    post_socket.bind(f"tcp://{args.ip}:{args.post_port}")
    pub_socket = context.socket(zmq.PUB)
    pub_socket.bind(f"tcp://{args.ip}:{args.pub_port}")

    while True:
        post_message = post_socket.recv_string()
        ServerData().add_message(post_message)
        post_socket.send_string("Post message transferred to the published channel.")
        if post_message:
            list_of_post_messages = post_message.split(",")
            pub_message = f"{list_of_post_messages[0]}: {list_of_post_messages[2]} ({list_of_post_messages[1]})"
            pub_socket.send_string(pub_message)
        
elif args.post_port.isnumeric() and 1024 <= int(args.post_port) <= 65535:
    print("Please, enter a valid server publishing port number (between 1024 and 65535, inclusive).")
elif args.pub_port.isnumeric() and 1024 <= int(args.pub_port) <= 65535:
    print("Please, enter a valid server posting port number (between 1024 and 65535, inclusive).")
else:
    print("Please, enter valid server posting and publishing port numbers (between 1024 and 65535, inclusive).")