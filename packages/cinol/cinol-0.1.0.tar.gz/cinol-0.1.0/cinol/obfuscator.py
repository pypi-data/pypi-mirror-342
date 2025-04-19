import ast  
import random  
import string  

def rename_identifiers(code):  
    tree = ast.parse(code)  
    # Ganti nama variabel/fungsi dengan string acak  
    for node in ast.walk(tree):  
        if isinstance(node, ast.Name):  
            node.id = ''.join(random.choices(string.ascii_lowercase, k=10))  
    return ast.unparse(tree)  
