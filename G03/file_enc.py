from Crypto.Cipher import AES
from Crypto.Cipher import ChaCha20
from Crypto.Util.Padding import pad
import os
import random
import struct
import string
import secrets


def encrypt_file_aes(key, filename, chunk_size=64*1024):
    output_filename = filename + '.encrypted'

    alphabet = string.ascii_letters + string.digits
    iv = ''.join(secrets.choice(alphabet) for i in range(16))
    encryptor = AES.new(key, AES.MODE_CBC,
                        iv=bytes(iv, "utf-8"))

    filesize = os.path.getsize(filename)
    with open(filename, 'rb') as inputfile:
        with open(output_filename, 'wb') as outputfile:
            outputfile.write(struct.pack('<Q', filesize))
            outputfile.write(bytes(iv, "utf-8"))
            while True:
                chunk = inputfile.read(chunk_size)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk = pad(chunk, AES.block_size)
                    #chunk += ' ' * (16 - len(chunk) % 16)
                outputfile.write(encryptor.encrypt(chunk))


def decrypt_file_aes(key, filename, chunk_size=24*1024):
    output_filename = os.path.splitext(filename)[0]

    with open(filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)
        with open(output_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunk_size)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate(origsize)


def encrypt_file_cha(key, filename, chunk_size=64*1024):
    output_filename = filename + '.encrypted'

    alphabet = string.ascii_letters + string.digits
    nonce = ''.join(secrets.choice(alphabet) for i in range(12))
    key = pad(key, 32)

    encryptor = ChaCha20.new(key=key, nonce=bytes(nonce, "utf-8"))
    filesize = os.path.getsize(filename)

    with open(filename, 'rb') as inputfile:
        with open(output_filename, 'wb') as outputfile:
            outputfile.write(struct.pack('<Q', filesize))
            outputfile.write(bytes(nonce, "utf-8"))
            while True:
                chunk = inputfile.read(chunk_size)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - len(chunk) % 16)
                outputfile.write(encryptor.encrypt(chunk))


def decrypt_file_cha(key, filename, chunk_size=24*1024):
    output_filename = os.path.splitext(filename)[0]

    with open(filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(12)
        decryptor = AES.new(key, AES.MODE_CBC, iv)
        with open(output_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunk_size)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate(origsize)


encrypt_file_aes(b'abcdefghji123456', 'texto.txt')

decrypt_file_aes(b'abcdefghji123456', 'texto.txt.encrypted')

encrypt_file_cha(b'abcdefghji123456', 'texto.txt')

decrypt_file_cha(b'abcdefghji123456', 'texto.txt.encrypted')
