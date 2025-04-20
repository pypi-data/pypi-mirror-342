import zlib
from argon2.low_level import hash_secret_raw, Type
from nacl.secret import SecretBox

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

def decrypt_file(input_path: str, output_path: str, password: str):
    """
    Decrypt and decompress a file encrypted with XChaCha20-Poly1305 and Argon2id.
    """
    with open(input_path, 'rb') as f:
        salt = f.read(ARGON2_SALT_LEN)
        nonce = f.read(NONCE_SIZE)
        ciphertext = f.read()
    key = derive_key(password.encode(), salt)
    box = SecretBox(key)
    try:
        compressed = box.decrypt(nonce + ciphertext)
        plaintext = zlib.decompress(compressed)
    except Exception as e:
        raise RuntimeError(f"Decryption failed: {e}")
    with open(output_path, 'wb') as f:
        f.write(plaintext)
