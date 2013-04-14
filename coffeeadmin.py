#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

# Payment
sys.path.insert(0, "coffeeserver/")
from payment import *
import coffeeserver
payment = coffeeserver.load_payment()

import webuser

import datetime

# Flask
from flask import *
from flask.ext.bootstrap import Bootstrap
from flask.ext.login import *
from flask.ext import admin
from flask.ext.admin.contrib import sqlamodel
from utils import *

app = Flask(__name__)
app.payment = payment
app.secret_key = ':D' # Change this ...

# stuff
def unix2datetime(unixtime):
    return datetime.fromtimestamp(int(unixtime))
app.jinja_env.globals.update(unix2datetime=unix2datetime)

# Bootstrap
Bootstrap(app)  
app.config['BOOTSTRAP_USE_CDN'] = False
app.config['BOOTSTRAP_FONTAWESOME'] = True

# Login manager
login_manager = LoginManager()
login_manager.setup_app(app)
login_manager.session_protection = "strong"
login_manager.anonymous_user = webuser.AnonymousUser

# Blueprints
import transactions
app.register_blueprint(transactions.transactions)
import itemtransactions
app.register_blueprint(itemtransactions.itemtransactions)
import login
app.register_blueprint(login.login)
import items
app.register_blueprint(items.items)
import wallets
app.register_blueprint(wallets.wallets)
import users
app.register_blueprint(users.users)
import tokens
app.register_blueprint(tokens.tokens)

# Admin
class CoffeeAdminIndexView(admin.AdminIndexView):
    def is_accessible(self):
        return current_user.is_admin()

class CoffeeModelView(sqlamodel.ModelView):
    def is_accessible(self):
        return current_user.is_admin()

admin = admin.Admin(app, 'Test', index_view=CoffeeAdminIndexView())
admin.add_view(CoffeeModelView(Item, payment.session))
admin.add_view(CoffeeModelView(Transaction, payment.session))
admin.add_view(CoffeeModelView(ItemTransaction, payment.session))
admin.add_view(CoffeeModelView(Token, payment.session))
admin.add_view(CoffeeModelView(User, payment.session))
admin.add_view(CoffeeModelView(Wallet, payment.session))

@app.route('/')
def index():
    return render('home.html')

# Login Manager stuff
@login_manager.unauthorized_handler
def unauthorized():
    return render('error.html', error_title='Nicht autorisiert', error_message='Um diese Seite anzusehen bitte einloggen.')

@login_manager.user_loader
def load_user(userid):
    return webuser.get(payment, userid)

# Catch-All
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    abort(404)

if __name__ == '__main__':
    app.run(debug=True)