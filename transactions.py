from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from utils import *

transactions = Blueprint('transactions', __name__, template_folder='templates')

@transactions.route('/transactions/')
@login_required
def transactionsf():
    return render('placeholder.html')