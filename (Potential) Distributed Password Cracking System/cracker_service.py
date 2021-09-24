from flask import Flask, request, jsonify
import json
import argparse
import itertools
import string
import hashlib


app = Flask(__name__)

cached_passwords = {}
first_characters = list(string.printable)
for char in first_characters:
    cached_passwords[char] = {}


def bruteforce_password(starting_character, hashed_password, password_length):
    global cached_passwords
    try:
        if cached_passwords[starting_character][password_length][hashed_password] == "None":
            return None
        else:
            return cached_passwords[starting_character][password_length][hashed_password]
    except KeyError:
        pass

    for guess in itertools.product(string.printable, repeat=password_length):
        result = ''.join(tuple(starting_character) + guess)
        if hashlib.md5(result.encode()).hexdigest() == hashed_password:
            if password_length not in cached_passwords[starting_character]:
                cached_passwords[starting_character][password_length] = {}
            cached_passwords[starting_character][password_length][hashed_password] = result
            return result

    if password_length not in cached_passwords[starting_character]:
        cached_passwords[starting_character][password_length] = {}
    cached_passwords[starting_character][password_length][hashed_password] = "None"
    return None


@app.route('/', methods=['PUT', 'POST'])
def add_info():
    requested_data = json.loads(request.data.decode())
    guess = bruteforce_password(requested_data['character'], requested_data['password'], requested_data['length'])
    return jsonify(guess=guess)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog = "cracker_service", description = "Cracker Service")
    parser.add_argument("port", help = "Please, enter the cracker web service port number between 1024 and 65535.")
    args = parser.parse_args()

    app.run(debug=True, port=args.port)
