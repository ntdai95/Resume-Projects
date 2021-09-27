import json


class Message:
    def __init__(self, action=None, success=None, message=None, username=None, password=None, 
                 email=None, filename=None, tag=None):
        self.action = action
        self.success = success
        self.message = message
        self.username = username
        self.password = password
        self.email = email
        self.filename = filename
        self.tag = tag


    def to_json(self):
        return json.dumps(vars(self)).encode(encoding="utf-8")


    @classmethod
    def process_message(cls, message):
        response = message.decode(encoding="utf-8")
        return json.loads(response)


    @classmethod
    def sending_file(cls, filename, client_socket, network_buffer_size):
        with open("{}.code".format(filename), "rb") as compressed_file:
            while True:
                bytes_data = compressed_file.read(network_buffer_size)
                if not bytes_data:
                    break
                client_socket.sendall(bytes_data)


    @classmethod
    def receiving_file(cls, filename, client_socket, network_buffer_size):
        with open("{}.code".format(filename), "wb") as compressed_file:
            while True:
                bytes_data = client_socket.recv(network_buffer_size)
                if not bytes_data:
                    break
                compressed_file.write(bytes_data)
