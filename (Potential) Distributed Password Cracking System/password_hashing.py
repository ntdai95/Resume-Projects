import hashlib
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog = "password hashing", description = "Password Hashing")
    parser.add_argument("password", help = "Please, type in the password that you want to hash.")
    args = parser.parse_args()

    print(hashlib.md5(args.password.encode()).hexdigest())