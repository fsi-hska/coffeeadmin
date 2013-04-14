from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from flask.ext.login import *
from utils import *
from payment import *

items = Blueprint('items', __name__, template_folder='templates')


@items.route('/items')
@items.route('/items/')
@items.route('/items/list')
@login_required
def items_list():
    i = current_app.payment.session.query(Item).order_by(Item.id.asc()).all()
    return render('items_list.html', items=i)

@items.route('/items/view/<int:id>')
@login_required
def items_view(id):
    i = current_app.payment.getItemById(id)
    if i is None:
        return render('error.html', error_title='Item nicht gefunden')
    return render('items_view.html', item=i)

@items.route('/items/buy')
@login_required
def items_buy():
    return render('items_buy.html', items=current_app.payment.getItems())

@items.route('/items/image/<int:item_id>')
@login_required
def item_image(item_id):
    item = current_app.payment.getItemById(item_id)
    if item is None:
        abort(404)
    else:
        return send_file('coffeeserver/resource/items/' + item.image, mimetype='image/png')