from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from utils import *
from payment import *

transactions = Blueprint('transactions', __name__, template_folder='templates')

@transactions.route('/transactions/')
@login_required
def transactionsf():
    t = current_app.payment.session.query(Transaction).order_by(Transaction.time.desc()).all()
    return render('transactions.html', transactions=t)