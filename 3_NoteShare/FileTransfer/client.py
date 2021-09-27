from socket import *
import os
from dotenv import load_dotenv
from models import Message


load_dotenv()
SERVER_IP = os.environ.get("SERVER_IP")
SERVER_PORT = int(os.environ.get("SERVER_PORT"))


class Client:
    __client_socket = socket(AF_INET, SOCK_STREAM)
    __client_socket.connect((SERVER_IP, SERVER_PORT))
    __network_buffer_size = 4096


    @classmethod
    def send_action_message(cls, data, filename=None, action=None):
        try:
            cls.__client_socket.sendall(data)
            if filename and action == "upload":
                Message.sending_file(filename=filename, client_socket=cls.__client_socket,
                                           network_buffer_size=cls.__network_buffer_size)
            elif filename and action == "download":
                Message.receiving_file(filename=filename, client_socket=cls.__client_socket,
                                             network_buffer_size=cls.__network_buffer_size)

            server_data_json = cls.__client_socket.recv(cls.__network_buffer_size)
            return Message.process_message(server_data_json)
        except:
            return {"success":False, "message":"Server is temporarily unavailable. Try again later!"}
        finally:
            cls.__client_socket.close()
            