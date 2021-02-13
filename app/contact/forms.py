from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField,

## contact form

class ContactForm(FlaskForm):

    name = StringField('Name:', id='name_contact', [DataRequired()])
    email = StringField('E-Mail:', id='mail_contact', [Email(message=('Not a valid E-Mail address.')),DataRequired()])
    body = TextAreaField('Message:', id='body_contact', [DataRequired(),Length(min=50, message=('Your message is too short.'))])
    recaptcha = RecaptchaField(id='recaptcha_contact')
    submit = SubmitField('Submit', id='submit_contact')


