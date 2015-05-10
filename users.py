from flask import Blueprint, render_template, abort
from flask.ext.login import login_required
from jinja2 import TemplateNotFound
from utils import *
from payment import *

users = Blueprint('users', __name__, template_folder='blueprints/users')

@users.route('/users')
@users.route('/users/list')
@login_required
def users_list():
    u = current_app.payment.session.query(User).order_by(User.id.asc()).all()
    return render('users_list.html', users=u)

@users.route('/users/view/<int:id>')
@login_required
def users_view(id):
    u = current_app.payment.getUserById(id)
    if u is None:
        return render('error.html', error_title='User nicht gefunden')
    return render('users_view.html', selected_user=u)