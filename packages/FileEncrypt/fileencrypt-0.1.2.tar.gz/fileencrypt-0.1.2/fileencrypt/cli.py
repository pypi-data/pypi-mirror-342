import sys
import argparse
from getpass import getpass
from fileencrypt.encrypt import encrypt_file
from fileencrypt.decrypt import decrypt_file

def main():
    parser = argparse.ArgumentParser(
        description="Encrypt or decrypt a file using XChaCha20-Poly1305 and Argon2id."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Encrypt subcommand
    encrypt_parser = subparsers.add_parser("encrypt", help="Encrypt a file")
    encrypt_parser.add_argument("input_file", help="Path to the input (plaintext) file.")
    encrypt_parser.add_argument("output_file", help="Path to the output (encrypted) file.")
    encrypt_parser.add_argument("password", nargs="?", help="Password to use for encryption (not recommended to provide on CLI for security reasons). If not provided, you will be prompted.")

    # Decrypt subcommand
    decrypt_parser = subparsers.add_parser("decrypt", help="Decrypt a file")
    decrypt_parser.add_argument("input_file", help="Path to the input (encrypted) file.")
    decrypt_parser.add_argument("output_file", help="Path to the output (decrypted) file.")
    decrypt_parser.add_argument("password", nargs="?", help="Password to use for decryption (not recommended to provide on CLI for security reasons). If not provided, you will be prompted.")

    args = parser.parse_args()

    if args.command == "encrypt":
        password = args.password or getpass("Enter password: ")
        encrypt_file(args.input_file, args.output_file, password)
    elif args.command == "decrypt":
        password = args.password or getpass("Enter password: ")
        try:
            decrypt_file(args.input_file, args.output_file, password)
            print(f"File decrypted and saved to {args.output_file}")
        except Exception as e:
            print(f"Decryption failed: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
