# -*- encoding: utf-8 -*-

from django.core.mail import send_mail
import smtplib
from gilbi.mistrael.helpers.encryption_helper import encrypt_login_email
from gilbi.mistrael.messages.email_messages import *
from gilbi.settings import DOMAIN_URL

def send_email(title, text, email):
    try:
        send_mail(
            subject = title,
            message = text,
            from_email = 'lar.de.mistrael.lb@gmail.com',
            recipient_list = [email],
            fail_silently = False
            )
    except smtplib.SMTPException:
        return False
    else:
        return True
    
def create_active_url(encrypted_login_email, id):
    url = DOMAIN_URL + "ativarconta/" + str(id) + "/" + encrypted_login_email
    return url

def create_disable_url(encrypted_login_email, id):
    url = DOMAIN_URL + "desativarconta/" + str(id) + "/" + encrypted_login_email
    return url

def create_change_password_url(encrypted_login_email, id):
    url = DOMAIN_URL + "mudarsenha/" + str(id) + "/" + encrypted_login_email
    return url    

def create_confirmation_email(login, email, id):
    code = encrypt_login_email(login, email)
    activate_link = create_active_url(code, id)
    disable_link = create_disable_url(code, id)
    message = MESSAGE_ACTIVE_ACCOUNT + activate_link + MESSAGE_DISABLE_ACCOUNT + disable_link
    return message

def create_change_password_email(login, email, id):
    code = encrypt_login_email(login, email)
    link = create_change_password_url(code, id)
    message = MESSAGE_CHANGE_ACCOUNT_PASSWORD + link
    return message