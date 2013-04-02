#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

# Payment
sys.path.insert(0, "coffeeserver/")
import coffeeserver
payment = coffeeserver.load_payment()

import user

# Flask
from flask import *
from flask.ext.bootstrap import Bootstrap
from flask.ext.login import *
app = Flask(__name__)
app.secret_key = ':D' # Change this ...

# Bootstrap
Bootstrap(app)
app.config['BOOTSTRAP_USE_CDN'] = False
app.config['BOOTSTRAP_FONTAWESOME'] = True

# Login manager
login_manager = LoginManager()
login_manager.setup_app(app)
login_manager.session_protection = "strong"
login_manager.anonymous_user = user.AnonymousUser

def render(link, **context):
    return render_template(link, user=current_user, **context)

@login_manager.user_loader
def load_user(userid):
    return user.get(payment, userid)

@app.route('/')
def index():
    return render('home.html')

@app.route('/items/')
@login_required
def items():
    return render('items.html', items=payment.getItems())

@app.route('/items/image/<int:item_id>')
@login_required
def item_image(item_id):
    item = payment.getItemById(item_id)
    if item is None:
        abort(404)
    else:
        return send_file('coffeeserver/resource/items/' + item.image, mimetype='image/png')

@app.route('/transactions/')
@login_required
def transactions():
    return render('placeholder.html')

# Register, Login and logout stuff
@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        error = {}
        values = {'username': request.form['username'], 'password': request.form['password'], 'email': request.form['email'], 'hs-user': request.form['hs-user'] }
        if not values['username']:
            error['username'] = "Darf nicht leer sein."
        if not values['password']:
            error['password'] = "Darf nicht leer sein."
        if not values['email']:
            error['email'] = "Darf nicht leer sein."
        if not values['hs-user']:
            error['hs-user'] = "Darf nicht leer sein."

        if len(error) > 0:
            return render('register.html', validation=True, error=error, values=values)
        else:
            payment.addUser(values['username'], values['password'], values['email'], values['hs-user'], None)
            return render('success.html', title="Erfolgreich registriert...", message="foo!")

    return render('register.html', validation=False)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    web_user = user.validate(payment, username, password)
    if web_user is not None:
        login_user(web_user)
        render('placeholder.html', message="login successful!")
    return render('placeholder.html', message="login unsuccessful!")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

# User not logged in error message
@login_manager.unauthorized_handler
def unauthorized():
    return render('error.html', error_title='Nicht autorisiert', error_message='Um diese Seite anzusehen bitte einloggen.')

# Catch-All
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    abort(404)

if __name__ == '__main__':
    app.run(debug=True)