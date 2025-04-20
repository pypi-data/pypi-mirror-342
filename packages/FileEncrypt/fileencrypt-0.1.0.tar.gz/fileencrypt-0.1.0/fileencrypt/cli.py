import sys
import argparse
from getpass import getpass
from fileencrypt.encrypt import encrypt_file

def main():
    parser = argparse.ArgumentParser(
        description="Encrypt a file using XChaCha20-Poly1305 and Argon2id."
    )
    parser.add_argument("input_file", help="Path to the input (plaintext) file.")
    parser.add_argument("output_file", help="Path to the output (encrypted) file.")
    parser.add_argument("password", nargs="?", help="Password to use for encryption (not recommended to provide on CLI for security reasons). If not provided, you will be prompted.")
    args = parser.parse_args()

    password = args.password
    if password is None:
        password = getpass("Enter password: ")
    encrypt_file(args.input_file, args.output_file, password)

if __name__ == "__main__":
    main()
