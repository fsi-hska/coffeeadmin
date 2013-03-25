#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from flask import *
from flask.ext.bootstrap import Bootstrap
from flask.ext.login import LoginManager
sys.path.insert(0, "coffeeserver/")
import coffeeserver

app = Flask(__name__)

# Bootstrap
Bootstrap(app)
app.config['BOOTSTRAP_USE_CDN'] = False
app.config['BOOTSTRAP_FONTAWESOME'] = True

# Payment
payment = coffeeserver.load_payment()


# Login manager
login_manager = LoginManager()
login_manager.setup_app(app)

@login_manager.user_loader
def load_user(userid):
    return None
    #return User.get(userid)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    return render_template('placeholder.html')

@app.route('/items/')
def items():
    return render_template('items.html', items=payment.getItems())

@app.route('/items/image/<int:item_id>')
def item_image(item_id):
    item = payment.getItemById(item_id)
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

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    abort(404)

if __name__ == '__main__':
    app.run(debug=True)