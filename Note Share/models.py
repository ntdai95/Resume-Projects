import json
import os


class Message:
    def __init__(self, action=None, success=None, message=None, username=None,
                 receiving_username=None, email_message=None, password=None,
                 email=None, filename=None, tag=None, topic=None):
        self.action = action
        self.success = success
        self.message = message
        self.username = username
        self.receiving_username = receiving_username 
        self.password = password
        self.email = email
        self.email_message = email_message
        self.filename = filename
        self.tag = tag
        self.topic = topic

    def to_json(self):
        return json.dumps(vars(self)).encode(encoding="utf-8")

    @classmethod
    def process_message(cls, message):
        response = message.decode(encoding="utf-8")
        return json.loads(response)

    @classmethod
    def sending_file(cls, filename, client_socket, network_buffer_size):
        filepath = os.path.join(os.path.dirname(__file__),
                                "{}.code".format(filename))
        with open(filepath, "rb") as compressed_file:
            while True:
                bytes_data = compressed_file.read(network_buffer_size)
                if not bytes_data:
                    return
                client_socket.sendall(bytes_data)

    @classmethod
    def receiving_file(cls, filename, client_socket, network_buffer_size):
        filepath = os.path.join(os.path.dirname(__file__),
                                "{}.code".format(filename))
        with open(filepath, "wb") as compressed_file:
            while True:
                bytes_data = client_socket.recv(network_buffer_size)
                if len(bytes_data) < network_buffer_size:
                    compressed_file.write(bytes_data)
                    return
                compressed_file.write(bytes_data)
