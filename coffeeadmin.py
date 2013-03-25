#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from flask import *
from flask.ext.bootstrap import Bootstrap
sys.path.insert(0, "coffeeserver/")
import coffeeserver

app = Flask(__name__)
Bootstrap(app)
app.config['BOOTSTRAP_USE_CDN'] = False
app.config['BOOTSTRAP_FONTAWESOME'] = True

p = coffeeserver.load_payment()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/items/')
def items():
    return render_template('items.html', items=p.getItems())

@app.route('/items/image/<int:item_id>')
def item_image(item_id):
    item = p.getItemById(item_id)
    if item is None:
        abort(404)
    else:
        return send_file('coffeeserver/resource/items/' + item.image, mimetype='image/png')

@app.route('/transactions/')
def transactions():
    return render_template('placeholder.html')

@app.route('/contact/')
def contact():
    return render_template('placeholder.html')

if __name__ == '__main__':
    app.run(debug=True)