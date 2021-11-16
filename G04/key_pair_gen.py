from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import base64

priv_path = input("Private key file name: ")
pub_path = input("Public key file name: ")

op = 0
size = 0
while op > 4 or op <= 0:
    op = int(input("Key size: [1]-1024\t[2]-2048\t[3]-3072\t[4]-4096\t: "))
    if op == 1:
        size = 1024
    elif op == 2:
        size = 2048
    elif op == 3:
        size = 3072
    else:
        size = 4096

private_key = rsa.generate_private_key(public_exponent=65537, key_size=size,)
public_key = private_key.public_key()

pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

with open(priv_path + ".pem", "w") as key_file:
    key_file.write(pem.decode("utf-8"))

pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

with open(pub_path + ".pem", "w") as key_file:
    key_file.write(pem.decode("utf-8"))
