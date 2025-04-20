# FileEncrypt

A simple Python package and CLI tool for encrypting files using XChaCha20-Poly1305 and Argon2id.
FileEncrypt focus on security, simplicity and reliability. It uses the secure XChaCha20 cipher and Argon2id key derivation function to provide a high level of security.

## Installation

Install locally (for development or pip install):

```bash
pip install .
```

## Usage

### As a CLI tool

After installation, you can use the CLI:

```bash
fileencrypt <input_file> <output_file> <password>
```

- If `<password>` is omitted, you will be prompted securely.
- **Warning:** Passing the password as a CLI argument may expose it to other users on the system (use with caution).

### As a Python module

You can also use the encryption functionality in your own scripts:

```python
from fileencrypt import encrypt_file

encrypt_file("input.txt", "output.enc", "your_password")
```

## Decryption

A similar interface is available for decryption (see `fileencrypt.decrypt_file`).

---

## Requirements
- Python 3.7+
- argon2-cffi
- pynacl

## License
MIT
