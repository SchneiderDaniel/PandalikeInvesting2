from flask import url_for, current_app
from .extensions import mail
from flask_mail import Message



# def sendResetEMail(user):
#     token = user.get_reset_token()
#     msg = Message('Password Reset Request',
#                   sender=current_app.config['MAIL_USERNAME'],
#                   recipients=[user.email])
#     msg.body = f''' To reset your password, visit the following link:
# {url_for('users.reset_token', token = token, _external = True)}
# If you did not make this request, then simply ignore this E-Mail amd no changes will be made.
# '''
#     mail.send(msg)
    

def sendEMailToAdmin(mailFrom, nameFrom, text):
    msg = Message('Contact Message form '+ nameFrom +' to pandalikeInvesting.com',
                  sender=mailFrom,
                  recipients=[current_app.config['MAIL_USERNAME']])
    msg.body = "The user: " + mailFrom+ " wrote to pandalikeInvesting.com: " + text
    mail.send(msg)


# def sendActivateEMail(user):
#     token = user.get_reset_token()
#     msg = Message('Activate Account Mail',
#                   sender=current_app.config['MAIL_USERNAME'],
#                   recipients=[user.email])
#     msg.body = f''' Your account was created. To activate your account, visit the following link:
# {url_for('users.activate', token = token, _external = True)}
# If you did not make this request, then simply ignore this E-Mail amd no changes will be made.
# '''
#     mail.send(msg)