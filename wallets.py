from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from utils import *
from payment import *

wallets = Blueprint('wallets', __name__, template_folder='templates')

@wallets.route('/wallets/view/<int:id>')
@login_required
def transactionsf(id):
    w = current_app.payment.getWalletById(id)
    if w is None:
        return render('error.html', error_title='Wallet nicht gefunden')
    return render('wallet_view.html', wallet=w)