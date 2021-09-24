import argparse
import requests
import json
import threading
import string
import time


class Program:
    def __init__(self, args) -> None:
        self.args = args
        self.list_of_ports = args.port.split(",")
        self.password_length = 1
        self.first_characters = list(string.printable)
        self.running = True
        self.start_time = None


    def port_validity_check(self) -> bool:
        for port in self.list_of_ports:
            if port.isnumeric() == False or 1024 > int(port) or 65535 < int(port):
                return False
        return True


    def worker_request(self, port, character, args) -> None:
        try:
            if self.running:
                password = {'character': character, 'password': args.md5_password, 'length': self.password_length}
                response = requests.post(f'http://localhost:{port}/', data=json.dumps(password))
                if response.json()["guess"]:
                    self.running = False
                    print(response.json()["guess"])
                    print(f"Took {round(time.time() - self.start_time, 2)} seconds.")
                else:
                    self.first_characters.remove(character)
                    if self.first_characters == []:
                        self.password_length += 1
                        self.first_characters = list(string.printable)
        except requests.exceptions.RequestException:
            self.list_of_ports.remove(port)


    def main(self) -> None:
        if self.port_validity_check:
            self.start_time = time.time()
            while self.running:
                list_of_threads = []
                for port, character in zip(self.list_of_ports, self.first_characters):
                    t = threading.Thread(target=self.worker_request, args=[port, character, self.args])
                    t.start()
                    list_of_threads.append(t)

                for thread in list_of_threads:
                    thread.join()

                if self.list_of_ports == []:
                    self.running = False
                    print("All servers are down.")
                elif self.password_length == int(self.args.max_password_length):
                    self.running = False
                    print("None of the words are matched with the hashed password.")
                    print(f"Took {round(time.time() - self.start_time, 2)} seconds.")
        else:
            print("Please, enter valid port numbers.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog = "client", description = "Client")
    parser.add_argument("port", help = "Please, enter the cracker web service port numbers between 1024 and 65535, separated by comma.")
    parser.add_argument("md5_password", help = "Please, enter a hashed password to crack.")
    parser.add_argument("max_password_length", help = "Please, enter the maximum length of characters to check against the hashed password.")
    args = parser.parse_args()

    Program(args).main()
