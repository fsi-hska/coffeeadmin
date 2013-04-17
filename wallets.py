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
@wallets.route('/wallets/view/<int:id>/')
@login_required
def wallets_view(id):
    w = current_app.payment.getWalletById(id)
    if w is None:
        return render('error.html', error_title='Wallet nicht gefunden')
    return render('wallets_view.html', wallet=w)

@wallets.route('/wallets/edit/<int:id>', methods=['POST'])
@wallets.route('/wallets/edit/<int:id>/', methods=['POST'])
@login_required
def wallets_edit(id):
    reason = str(request.form['reason'])
    balance = request.form['balance']

    if len(reason) == 0:
        session['info'] = ['Yay!', 'Wallet-Balance nicht geaendert: Kein Grund angegeben!', 'error']
        return redirect('/wallets/view/' + str(id))

    try:    
        balance = int(balance)
    except:
        session['info'] = ['Yay!', 'Wallet-Balance nicht geaendert: Balance not int!', 'error']
        return redirect('/wallets/view/' + str(id))

    w = current_app.payment.getWalletById(id)
    if w is None:
        return render('error.html', error_title='Wallet nicht gefunden')

    w.transactions.append(Transaction(int(time.time()), balance, current_user.user.username + ' changed balance from ' + str(w.balance) + ' to ' + str(balance) + ': ' + str(reason)))
    w.balance = balance

    current_app.payment.session.commit()
    session['info'] = ['Yay!', 'Wallet-Balance geaendert!', 'success']
    return redirect('/wallets/view/' + str(id))