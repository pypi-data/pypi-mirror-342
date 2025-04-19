import hashlib  
import sys  

def verify_checksum(file_path: str, expected_hash: str) -> bool:  
    """Check if file is modified."""  
    with open(file_path, 'rb') as f:  
        file_hash = hashlib.sha256(f.read()).hexdigest()  
    return file_hash == expected_hash  

def exit_if_debugging():  
    """Terminate if running in debug mode."""  
    if sys.gettrace() is not None:  # Sedang di-debug  
        sys.exit("Debugging detected! Aborting.")  
