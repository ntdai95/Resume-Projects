from socket import *
import os
from dotenv import load_dotenv


load_dotenv()
SERVER_IP = os.environ.get("SERVER_IP")
SERVER_PORT = int(os.environ.get("SERVER_PORT"))

class Client:
    def __init__(self):
        self.__client_socket = socket(AF_INET, SOCK_STREAM)
        self.__client_socket.connect((SERVER_IP, SERVER_PORT))
        self.__network_buffer_size = 4096


    def send_action_message(self, data):
        self.__client_socket.sendall(data)
        server_data_json = self.__client_socket.recv(self.__network_buffer_size)
        self.__client_socket.close()
        return server_data_json


    def send_file(self, filename):
        self.__client_socket.send(filename.encode(encoding="utf-8"))
        with open(f"{filename}.code", "rb") as compressed_file:
            while True:
                bytes_data = compressed_file.read(self.__network_buffer_size)
                if not bytes_data:
                    break
                self.__client_socket.sendall(bytes_data)
                
        self.__client_socket.close()
            