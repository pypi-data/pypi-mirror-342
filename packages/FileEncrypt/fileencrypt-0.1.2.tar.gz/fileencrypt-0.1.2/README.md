# FileEncrypt

A simple Python package and CLI tool for encrypting and decrypting files using XChaCha20-Poly1305 and Argon2id.
FileEncrypt focuses on security, simplicity, and reliability. It uses the secure XChaCha20 cipher and Argon2id key derivation function to provide a high level of security.

## Installation

Install from PyPI:

```bash
pip install fileencrypt
```

Or install locally (for development):

```bash
pip install .
```

## Usage

### As a CLI tool

After installation, you can use the CLI for both encryption and decryption:

#### Encrypt a file
```bash
fileencrypt encrypt <input_file> <output_file> <password>
```
- If `<password>` is omitted, you will be prompted securely.

#### Decrypt a file
```bash
fileencrypt decrypt <input_file> <output_file> <password>
```
- If `<password>` is omitted, you will be prompted securely.

**Warning:** Passing the password as a CLI argument may expose it to other users on the system (use with caution).

### As a Python module

You can also use the encryption and decryption functionality in your own scripts:

```python
from fileencrypt import encrypt_file, decrypt_file

encrypt_file("input.txt", "output.enc", "your_password")
decrypt_file("output.enc", "decrypted.txt", "your_password")
```

---

## Requirements
- Python 3.7+
- argon2-cffi
- pynacl

## License
MIT

## Project Links
- Source: https://github.com/jordanbmrd/file-encrypt
- Issue Tracker: https://github.com/jordanbmrd/file-encrypt/issues
