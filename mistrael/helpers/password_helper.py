import hashlib

def encrypt_password(password):
    encrypted_password = hashlib.sha224(password).hexdigest()
    return encrypted_password

def compare_passwords(password, encrypted_password):
    if(encrypt_password(password) == encrypted_password):
        return True
    else:
        return False