import hashlib
from base64 import b64encode
from Crypto import Cipher
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

buffer_size = 65536


def file_enc(key_path, path_in):

    key = get_random_bytes(32)

    in_file = open(path_in, "rb")
    out_file = open(path_in + ".enc", "wb")

    cipher_encrypt = AES.new(key, AES.MODE_CFB)

    rsa = RSA.import_key(open(key_path).read())
    rsa_cipher = PKCS1_OAEP.new(rsa)
    sec_key = rsa_cipher.encrypt(key)
    out_file.write(sec_key)

    out_file.write(cipher_encrypt.iv)

    buffer = in_file.read(buffer_size)
    while len(buffer) > 0:
        ciphered_bytes = cipher_encrypt.encrypt(buffer)
        out_file.write(ciphered_bytes)
        buffer = in_file.read(buffer_size)

    in_file.close()
    out_file.close()


def file_dec(key_path, path_in):
    in_file = open(path_in, 'rb')
    out_file = open(path_in + '.dec', 'wb')

    rsa = RSA.import_key(open(key_path).read())
    rsa_cipher = PKCS1_OAEP.new(rsa)
    key = rsa_cipher.decrypt(in_file.read(rsa.size_in_bytes()))

    iv = in_file.read(16)

    cipher_encrypt = AES.new(key, AES.MODE_CFB, iv=iv)

    buffer = in_file.read(buffer_size)
    while len(buffer) > 0:
        decrypted_bytes = cipher_encrypt.decrypt(buffer)
        out_file.write(decrypted_bytes)
        buffer = in_file.read(buffer_size)

    in_file.close()
    out_file.close()


def compare_hash(path_in):
    block_size = 65536
    file_hash = hashlib.sha256()
    with open(path_in, "rb") as f:
        fb = f.read(block_size)
        while len(fb) > 0:
            file_hash.update(fb)
            fb = f.read(block_size)
    return file_hash.hexdigest()


file_enc("pub.pem", "texto.txt")

file_dec("priv.pem", "texto.txt.enc")