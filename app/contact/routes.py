from . import blueprint
from flask import render_template,flash, redirect, url_for
from .forms import ContactForm
from app.mail_util import sendEMailToAdmin

# @blueprint.route('/')
# def index():
#     return render_template('contact.html')


@blueprint.route('/', methods=['GET', 'POST'])
def index():
    contact_form = ContactForm()
    if contact_form.validate_on_submit():

        sendEMailToAdmin(contact_form.email.data,contact_form.name.data,contact_form.body.data)
        flash(
            f'Thanks {contact_form.name.data}, we have received your message. We will respond soon!', 'success')
        return redirect(url_for( 'home_blueprint.index'))

    return render_template('contact.html', contact_form=contact_form)
