import os
import zlib
from argon2.low_level import hash_secret_raw, Type
from nacl.secret import SecretBox
from nacl.utils import random as nacl_random

# Argon2id parameters
ARGON2_TIME_COST = 4  # 4 iterations
ARGON2_MEMORY_COST = 2 ** 16  # 64 MiB
ARGON2_PARALLELISM = 2  # 2 threads
ARGON2_HASH_LEN = 32  # 32 bytes hash length
ARGON2_SALT_LEN = 16  # 16 bytes salt length
NONCE_SIZE = 24  # 24 bytes nonce size

def derive_key(password: bytes, salt: bytes) -> bytes:
    """
    Derive a key from the password and salt using Argon2id.
    """
    return hash_secret_raw(
        secret=password,
        salt=salt,
        time_cost=ARGON2_TIME_COST,
        memory_cost=ARGON2_MEMORY_COST,
        parallelism=ARGON2_PARALLELISM,
        hash_len=ARGON2_HASH_LEN,
        type=Type.ID
    )

def encrypt_file(input_path: str, output_path: str, password: str):
    """
    Compress, encrypt, and save a file using XChaCha20-Poly1305 and Argon2id.
    """
    salt = os.urandom(ARGON2_SALT_LEN)
    nonce = nacl_random(NONCE_SIZE)
    key = derive_key(password.encode(), salt)
    box = SecretBox(key)

    with open(input_path, 'rb') as f:
        plaintext = f.read()
    compressed = zlib.compress(plaintext)
    ciphertext = box.encrypt(compressed, nonce)

    # Output format: [salt][nonce][ciphertext]
    with open(output_path, 'wb') as f:
        f.write(salt)
        f.write(nonce)
        f.write(ciphertext.ciphertext)
    print(f"File compressed, encrypted and saved to {output_path}")
