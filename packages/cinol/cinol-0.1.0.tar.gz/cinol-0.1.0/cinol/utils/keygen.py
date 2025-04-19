from Crypto.PublicKey import RSA  

def generate_rsa_keys():  
    """Generate RSA key pair for license signing."""  
    key = RSA.generate(2048)  
    private_key = key.export_key()  
    public_key = key.publickey().export_key()  
    return private_key, public_key  
