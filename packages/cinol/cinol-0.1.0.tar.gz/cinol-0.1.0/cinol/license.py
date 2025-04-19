from Crypto.PublicKey import RSA  
from Crypto.Signature import pkcs1_15  
from Crypto.Hash import SHA256  
from Crypto.Cipher import AES  
import base64  
import json  

class LicenseManager:  
    def __init__(self, private_key=None, public_key=None):  
        self.private_key = private_key  
        self.public_key = public_key  

    def generate_license(self, user_data: dict, expiration: str) -> str:  
        """  
        Generate encrypted license file (AES + RSA Signature).  
        Format: {data, signature, checksum}.  
        """  
        # Serialize data  
        license_data = {  
            "user": user_data,  
            "expiry": expiration  
        }  
        data_str = json.dumps(license_data)  

        # Encrypt with AES  
        aes_key = b'16-byte-aes-key!'  # Replace with dynamic key  
        cipher = AES.new(aes_key, AES.MODE_GCM)  
        ciphertext, tag = cipher.encrypt_and_digest(data_str.encode())  

        # Sign with RSA  
        if self.private_key:  
            h = SHA256.new(ciphertext + tag)  
            signature = pkcs1_15.new(self.private_key).sign(h)  
        else:  
            signature = b''  

        # Package license  
        license_pkg = {  
            "nonce": base64.b64encode(cipher.nonce).decode(),  
            "ciphertext": base64.b64encode(ciphertext).decode(),  
            "tag": base64.b64encode(tag).decode(),  
            "signature": base64.b64encode(signature).decode()  
        }  
        return json.dumps(license_pkg)  

    def validate_license(self, license_file: str) -> bool:  
        """Verify license integrity and signature."""  
        try:  
            license_data = json.loads(license_file)  
            nonce = base64.b64decode(license_data["nonce"])  
            ciphertext = base64.b64decode(license_data["ciphertext"])  
            tag = base64.b64decode(license_data["tag"])  
            signature = base64.b64decode(license_data["signature"])  

            # Decrypt  
            aes_key = b'16-byte-aes-key!'  
            cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)  
            data = cipher.decrypt_and_verify(ciphertext, tag)  

            # Verify RSA signature  
            if self.public_key:  
                h = SHA256.new(ciphertext + tag)  
                pkcs1_15.new(self.public_key).verify(h, signature)  

            return True  
        except (ValueError, KeyError):  
            return False  
