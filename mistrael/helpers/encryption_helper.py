import hashlib

def encrypt_login_email(login, email):
    login_email = login + email
    encrypted_login_email = hashlib.sha224(login_email).hexdigest()
    return encrypted_login_email