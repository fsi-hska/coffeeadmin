from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from utils import *
from payment import *

tokens = Blueprint('tokens', __name__, template_folder='blueprints/tokens')

@tokens.route('/tokens')
@tokens.route('/tokens/')
@tokens.route('/tokens/list')
@login_required
def tokens_list():
    t = current_app.payment.session.query(Token).order_by(Token.id.desc()).all()
    return render('tokens_list.html', tokens=t)