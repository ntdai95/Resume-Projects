from socket import *
import threading
import os
from dotenv import load_dotenv
from database import Database
from models import Message, Result


load_dotenv()
SERVER_IP = os.environ.get("SERVER_IP")
SERVER_PORT = int(os.environ.get("SERVER_PORT"))

class ClientThread(threading.Thread):
    def __init__(self, client_socket, client_address):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.client_address = client_address
        self.network_buffer_size = 4096
        self.db = Database(name="noteshare")
        

    def run(self):
        while True:
            client_message_raw = self.client_socket.recv(self.network_buffer_size)
            try:
                client_message = Message.process_message(client_message_raw)
                if client_message["action"] == "login":
                    if self.db.login(client_message["username"], client_message["password"]):
                        success_result = True
                    else:
                        success_result = False
                elif client_message["action"] == "register":
                    if self.db.register(client_message["username"], client_message["password"], client_message["email"]):
                        success_result = True
                    else:
                        success_result = False
                elif client_message["action"] == "password":
                    pass
                elif client_message["action"] == "upload":
                    pass
                elif client_message["action"] == "get_all":
                    pass
                elif client_message["action"] == "download":
                    pass
                self.client_socket.sendall(Result(success=success_result).to_json())
            except:
                filename = client_message_raw.decode(encoding="utf-8")
                with open(f"{filename}.code", "wb") as compressed_file:
                    while True:
                        bytes_data = self.client_socket.recv(self.network_buffer_size)
                        if not bytes_data:
                            break
                        compressed_file.write(bytes_data)
            finally:
                self.client_socket.close()
            

class Server:
    def __init__(self):
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.bind((SERVER_IP, SERVER_PORT))
        self.server_socket.listen(5)


    def run(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            t = ClientThread(client_socket, client_address)
            t.start()


if __name__ == '__main__':
    Server().run()