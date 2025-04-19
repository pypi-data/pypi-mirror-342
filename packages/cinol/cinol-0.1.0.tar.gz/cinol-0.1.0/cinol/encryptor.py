from Crypto.Cipher import AES  
import py_compile  

def encrypt_pyc(source_file, output_file, key):  
    # Kompilasi ke .pyc  
    py_compile.compile(source_file, cfile=output_file)  
    # Enkripsi file .pyc  
    cipher = AES.new(key, AES.MODE_GCM)  
    with open(output_file, 'rb') as f:  
        data = f.read()  
    ciphertext, tag = cipher.encrypt_and_digest(data)  
    with open(output_file + '.enc', 'wb') as f:  
        f.write(cipher.nonce + tag + ciphertext)  
