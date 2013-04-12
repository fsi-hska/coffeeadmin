from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from flask.ext.login import *
from utils import *

items = Blueprint('items', __name__, template_folder='templates')

@items.route('/items/')
@login_required
def itemsf():
    return render('items.html', items=current_app.payment.getItems())

@items.route('/items/image/<int:item_id>')
@login_required
def item_image(item_id):
    item = current_app.payment.getItemById(item_id)
    if item is None:
        abort(404)
    else:
        return send_file('coffeeserver/resource/items/' + item.image, mimetype='image/png')