from apps import app
from flask_mail import Message
from config.config import mail
from flask import request,jsonify

def send_email(recipient,subject,message_body):
    try:
        msg = Message(subject=subject,
                    sender=app.config['MAIL_USERNAME'],
                    recipients=[recipient])
        msg.body = message_body

        mail.send(msg)

        return True                
        
    except Exception as e:
        print("An error occurred: " + str(e))
        return False