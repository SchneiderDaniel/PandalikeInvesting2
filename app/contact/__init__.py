from flask import Blueprint

blueprint = Blueprint(
    'contact_blueprint',
    __name__,
    url_prefix='/contact',
    template_folder='templates',
    static_folder='static'
)
