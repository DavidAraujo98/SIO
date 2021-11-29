import getpass
from sys import argv
from base64 import b64encode
from Crypto.Util.Padding import pad, unpad
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import MD5, SHA3_512, SHA3_384, SHA3_256
from Crypto.Cipher import AES, DES3, ChaCha20
from Crypto.Random import get_random_bytes

def enc_sz(op):
    h = 64
    if (op == "DES3"):
        h = 16
    elif (op == "AES128"):
        h = 16
    elif (op == "ChaCha20"):
        h = 32
    return h

def hash_gen(op):
    h = MD5
    if (h == "SHA512"):
        h = SHA3_512
    elif (h == "SHA384"):
    	h = SHA3_384
    elif (h == "SHA3256"):
    	h = SHA3_256

def key_gen(hs, enc):
    p = getpass.getpass()
    salt = get_random_bytes(16)
    
    hs = hash_gen(hs)
    sz = enc_sz(enc)
    
    keys = PBKDF2(p, salt, sz, count=1000000, hmac_hash_module=hs)
    
    return keys

def DES3_enc(key, path):
    cipher = DES3.new(key, DES3.MODE_CBC)
    with open(path, "rb") as in_f:
        with open(path + ".enc", "wb") as out_f:
            data = in_f.read(DES3.block_size)
            while len(data) > 0:
                if len(data) < DES3.block_size:
                    data = pad(data, DES3.block_size)
                    bk = False
                data = cipher.encrypt(data)
                out_f.write(b64encode(data))
                data = in_f.read(DES3.block_size)

def AES128_enc(key, path):
    cipher = AES.new(key, AES.MODE_CBC)
    with open(path, "rb") as in_f:
        with open(path + ".enc", "wb") as out_f:
            data = in_f.read(AES.block_size)
            while len(data) > 0:
                if len(data) < AES.block_size:
                    data = pad(data, AES.block_size)
                    break;
                data = cipher.encrypt(data)
                out_f.write(b64encode(data))
                data = in_f.read(AES.block_size)

# ChaCha20

def enc_file(hs, enc, ph):
    key = key_gen(hs, enc)
    
    if(enc == "DES3"):
    	DES3_enc(key, ph)
    elif(enc == "AES128"):
    	AES128_enc(key, ph)
    elif(enc == "ChaCha20"):
    	ChaCha20_enc(key, ph)

enc_file(argv[1], argv[2], argv[3])
