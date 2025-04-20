from setuptools import setup, find_packages
import os

with open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="FileEncrypt",
    version="0.1.2",
    description="File compression, encryption and decryption using XChaCha20 cipher and Argon2id (CLI and Python module)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="dorit",
    url="https://github.com/jordanbmrd/file-encrypt",
    project_urls={
        "Source": "https://github.com/jordanbmrd/file-encrypt",
        "Tracker": "https://github.com/jordanbmrd/file-encrypt/issues"
    },
    packages=find_packages(),
    install_requires=[
        "argon2-cffi",
        "pynacl"
    ],
    entry_points={
        "console_scripts": [
            "fileencrypt=fileencrypt.cli:main"
        ]
    },
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
