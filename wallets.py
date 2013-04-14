from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from utils import *
from payment import *

wallets = Blueprint('wallets', __name__, template_folder='blueprints/wallets')

@wallets.route('/wallets')
@wallets.route('/wallets/list')
@login_required
def wallets_list():
    w = current_app.payment.session.query(Wallet).order_by(Wallet.id.asc()).all()
    return render('wallets_list.html', wallets=w)

@wallets.route('/wallets/view/<int:id>')
@login_required
def wallets_view(id):
    w = current_app.payment.getWalletById(id)
    if w is None:
        return render('error.html', error_title='Wallet nicht gefunden')
    return render('wallets_view.html', wallet=w)

@wallets.route('/wallets/edit/<int:id>/', methods=['POST'])
@login_required
def wallets_edit(id):
    balance = request.form['balance']
    reason = request.form['reason']

    print url_for('wallets_view', id=id)
    return

    try:
        balance = int(balance)
    except:
        return render('error.html', error_title='Balance is not int.')

    w = current_app.payment.getWalletById(id)
    if w is None:
        return render('error.html', error_title='Wallet nicht gefunden')
    return render('wallets_view.html', wallet=w)