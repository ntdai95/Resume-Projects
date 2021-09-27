from socket import *
import os
from dotenv import load_dotenv
from models import ClientMessage, ServerMessage


load_dotenv()
SERVER_IP = os.environ.get("SERVER_IP")
SERVER_PORT = int(os.environ.get("SERVER_PORT"))


class Client:
    def __init__(self):
        self.__client_socket = socket(AF_INET, SOCK_STREAM)
        self.__client_socket.connect((SERVER_IP, SERVER_PORT))
        self.__network_buffer_size = 4096


    def send_action_message(self, data, filename=None, action=None):
        try:
            self.__client_socket.sendall(data)
            if filename and action == "upload":
                ClientMessage.sending_file(filename=filename, client_socket=self.__client_socket,
                                           network_buffer_size=self.__network_buffer_size)
            elif filename and action == "download":
                ServerMessage.receiving_file(filename=filename, client_socket=self.__client_socket,
                                             network_buffer_size=self.__network_buffer_size)

            server_data_json = self.__client_socket.recv(self.__network_buffer_size)
            return ServerMessage.process_message(server_data_json)
        except:
            return {"success":False, "message":"Server is temporarily unavailable. Try again later!"}
        finally:
            self.__client_socket.close()
            