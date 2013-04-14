from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from utils import *
from payment import *

itemtransactions = Blueprint('itemtransactions', __name__, template_folder='templates')

@itemtransactions.route('/itemtransactions')
@itemtransactions.route('/itemtransactions/')
@itemtransactions.route('/itemtransactions/list')
@login_required
def itemtransactions_list():
    t = current_app.payment.session.query(ItemTransaction).order_by(ItemTransaction.time.desc()).all()
    return render('itemtransactions_list.html', itemtransactions=t)