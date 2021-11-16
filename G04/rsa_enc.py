from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes
import base64

in_path = input("Original file: ")
out_path = input("Output file: ")
pub_path = input("Public key file: ")

# Load pub key
pub_key = ""
with open(pub_path, "rb") as key_file:
    pub_key = serialization.load_pem_public_key(
        key_file.read(),
        backend=None,
    )
block_sz = (len(pub.key) / 8) - 11

body = ""
with open(in_path, "rb") as in_file:
    endloop = False
    while not endloop:
        block = in_file.read(block_sz)

        if len(block) % block_sz != 0:
            endloop = True
            padding.PKCS1v15(
                key=pub_key,
                hash_algorithm=hashes.SHA384()
            ).padder()


ciphertext = public_key.encrypt(
    message,
)
