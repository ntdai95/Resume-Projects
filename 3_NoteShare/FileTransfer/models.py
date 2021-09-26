import json
from abc import ABC, abstractmethod, abstractclassmethod


class AbstractBaseClassModel(ABC):
    def to_json(self):
        return json.dumps(vars(self)).encode(encoding="utf-8")


    def process_message(cls, message):
        response = message.decode(encoding="utf-8")
        return json.loads(response)


    def sending_file(cls, filename, client_socket, network_buffer_size):
        with open(f"{filename}.code", "rb") as compressed_file:
            while True:
                bytes_data = compressed_file.read(network_buffer_size)
                if not bytes_data:
                    break
                client_socket.sendall(bytes_data)


    def receiving_file(cls, filename, client_socket, network_buffer_size):
        with open(f"{filename}.code", "wb") as compressed_file:
            while True:
                bytes_data = client_socket.recv(network_buffer_size)
                if not bytes_data:
                    break
                compressed_file.write(bytes_data)


class ClientMessage(AbstractBaseClassModel):
    def __init__(self, action, username=None, password=None, 
                 email=None, filename=None, tag=None):
        self.action = action
        self.username = username
        self.password = password
        self.email = email
        self.filename = filename
        self.tag = tag


    @abstractmethod
    def to_json(self):
        return super().to_json()


    @abstractclassmethod
    def process_message(cls, message):
        return super().process_message(message)


    @abstractclassmethod
    def sending_file(cls, filename, client_socket, network_buffer_size):
        return super().sending_file(filename, client_socket, network_buffer_size)


    @abstractclassmethod
    def receiving_file(cls, filename, client_socket, network_buffer_size):
        return super().receiving_file(filename, client_socket, network_buffer_size)


class ServerMessage(AbstractBaseClassModel):
    def __init__(self, success, message=None):
        self.success = success
        self.message = message


    @abstractmethod
    def to_json(self):
        return super().to_json()


    @abstractclassmethod
    def process_message(cls, message):
        return super().process_message(message)


    @abstractclassmethod
    def sending_file(cls, filename, client_socket, network_buffer_size):
        return super().sending_file(filename, client_socket, network_buffer_size)


    @abstractclassmethod
    def receiving_file(cls, filename, client_socket, network_buffer_size):
        return super().receiving_file(filename, client_socket, network_buffer_size)
