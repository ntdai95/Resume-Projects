import os
from dotenv import load_dotenv
from socket import socket, AF_INET, SOCK_STREAM
from models import Message


load_dotenv()
SERVER_IP = os.environ.get("SERVER_IP")
SERVER_PORT = int(os.environ.get("SERVER_PORT"))


class Client:
    def __init__(self) -> None:
        self.__client_socket = socket(AF_INET, SOCK_STREAM)
        self.__client_socket.connect((SERVER_IP, SERVER_PORT))
        self.__buffer_size = 4096

    def send_action_message(self, data=None):
        try:
            self.__client_socket.sendall(data)
            server_data_json = self.__client_socket.recv(self.__buffer_size)
            server_message = Message.process_message(server_data_json)
            if server_message["success"] and server_message["message"] == "Your note has been uploaded!":
                Message.sending_file(filename=server_message["filename"],
                                     client_socket=self.__client_socket,
                                     network_buffer_size=self.__buffer_size)
            elif server_message["success"] and server_message["message"] == "Your note has been donwloaded!":
                Message.receiving_file(filename=server_message["filename"],
                                       client_socket=self.__client_socket,
                                       network_buffer_size=self.__buffer_size)
        except:
            server_message = {"success": False,
                              "message": "Server is temporarily "
                                         "unavailable. Try again later!"}
        finally:
            self.__client_socket.close()
            return server_message
