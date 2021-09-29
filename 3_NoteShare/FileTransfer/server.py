import os
import threading
import smtplib
import hashlib
import pytz
from datetime import datetime
from socket import *
from dotenv import load_dotenv
from database import Database
from models import Message


load_dotenv()
EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
SERVER_IP = os.environ.get("SERVER_IP")
SERVER_PORT = int(os.environ.get("SERVER_PORT"))


class ClientThread(threading.Thread):
    def __init__(self, client_socket):
        threading.Thread.__init__(self)
        self.__client_socket = client_socket
        self.__network_buffer_size = 4096
        self.__db = Database(name="NoteShare")
        self.__run()
    

    def __send_email(self, email, username=None, password=None):
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            if email and username and password:
                subject = 'Request to change your password!'
                body = "Please, use the following new credentials to login to NoteShare:\n\nUsername: {}\nPassword: {}".format(username, password)
            elif email:
                subject = 'NoteShare registration successful!'
                body = "Welcome to NoteShare!\n\nThank you for registering! Feel free to start getting or sharing your notes with others."
            message = "Subject: {}\n\n{}".format(subject, body)
            smtp.sendmail(EMAIL_ADDRESS, email, message)


    def __run(self):
        client_message_raw = self.__client_socket.recv(self.__network_buffer_size)
        client_message = Message.process_message(client_message_raw)
        if client_message["password"]:
            hashed_password = hashlib.sha256(client_message["password"].encode()).hexdigest()

        if client_message["action"] == "login":
            success_result, message_result = self.__db.login(username=client_message["username"], 
                                                             password=hashed_password)
        elif client_message["action"] == "register":
            success_result, message_result = self.__db.register(username=client_message["username"],
                                                                password=hashed_password,
                                                                email=client_message["email"])
            if success_result:
                self.__send_email(email=client_message["email"])
        elif client_message["action"] == "password email":
            success_result, message_result, username = self.__db.update_password_email(email=client_message["email"],
                                                                                        new_password=hashed_password)
            if success_result:
                self.__send_email(email=client_message["email"], username=username, password=client_message["password"])
        elif client_message["action"] == "password username":
            success_result, message_result = self.__db.update_password_username(username=client_message["username"],
                                                                                new_password=hashed_password)
        elif client_message["action"] == "get all files":
            success_result, message_result = self.__db.get_all_notes()
        elif client_message["action"] == "upload":
            success_result, message_result = self.__db.add_note(filename=client_message["filename"],
                                                                username=client_message["username"],
                                                                tag=client_message["tag"],
                                                                created=datetime.now(pytz.timezone("America/Chicago")).strftime("%Y-%m-%d"))
        elif client_message["action"] == "download":
            success_result, message_result = True, "Your note has been donwloaded!"


        if client_message["action"] == "upload" or client_message["action"] == "download":
            self.__client_socket.sendall(Message(success=success_result, message=message_result,
                                                 filename=client_message["filename"]).to_json())
        else:    
            self.__client_socket.sendall(Message(success=success_result, message=message_result).to_json())


        if success_result and client_message["action"] == "upload":
            Message.receiving_file(filename=client_message["filename"], client_socket=self.__client_socket,
                                   network_buffer_size=self.__network_buffer_size)
        elif client_message["action"] == "download":
            Message.sending_file(filename=client_message["filename"], client_socket=self.__client_socket, 
                                 network_buffer_size=self.__network_buffer_size)
        self.__client_socket.close()
            

class Server:
    __server_socket = socket(AF_INET, SOCK_STREAM)
    __server_socket.bind((SERVER_IP, SERVER_PORT))
    __server_socket.listen(1)


    @classmethod
    def run(cls):
        while True:
            client_socket, client_address = cls.__server_socket.accept()
            t = ClientThread(client_socket)
            t.start()


if __name__ == '__main__':
    Server.run()
