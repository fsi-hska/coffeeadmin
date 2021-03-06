from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from utils import *
from payment import *
from flask.ext.login import login_required

transactions = Blueprint('transactions', __name__, template_folder='blueprints/transactions')

@transactions.route('/transactions')
@transactions.route('/transactions/')
@transactions.route('/transactions/list')
@login_required
def transactions_list():
    t = current_app.payment.session.query(Transaction).order_by(Transaction.time.desc()).all()
    return render('transactions_list.html', transactions=t)