import sys  
from Crypto.Cipher import AES  

def load_encrypted_module(enc_file, key):  
    with open(enc_file, 'rb') as f:  
        nonce, tag, ciphertext = [f.read(x) for x in (16, 16, -1)]  
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)  
    bytecode = cipher.decrypt_and_verify(ciphertext, tag)  
    # Eksekusi bytecode di memori (tanpa file)  
    exec(bytecode, sys.modules['__main__'].__dict__)  
