from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from flask.ext.login import *
from utils import *
import re
import webuser

login = Blueprint('login', __name__, template_folder='templates')

# Register, Login and logout stuff
@login.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        error = {}
        values = {'username': request.form['username'], 
                  'password': request.form['password'], 
                  'email': request.form['email'], 
                  'hs-user': request.form['hs-user'],
                  'cc-id': request.form['cc-id'] }

        if not values['username']:
            error['username'] = "Darf nicht leer sein."
        if not values['password']:
            error['password'] = "Darf nicht leer sein."
        if not values['email']:
            error['email'] = "Darf nicht leer sein."
        if not values['hs-user']:
            error['hs-user'] = "Darf nicht leer sein."
        else:
            p = re.compile('^[a-z]{4}[0-9]{4}$')
            if p.match(values['hs-user']) is None:
                error['hs-user'] = "Falsches Format."
        if not values['cc-id']:
            error['cc-id'] = "Darf nicht leer sein."
        else:
            p = re.compile('^[0-9]{4}\-[0-9]{8}$')
            if p.match(values['cc-id']) is None:
                error['cc-id'] = "Falsches Format."

        if len(error) > 0:
            return render('register.html', validation=True, error=error, values=values)
        else:
            current_app.payment.addUser(values['username'], values['password'], values['email'], values['hs-user'], None)
            return render('success.html', title="Erfolgreich registriert...", message="foo!")

    return render('register.html', validation=False)

@login.route('/login', methods=['POST'])
def loginf():
    username = request.form['username']
    password = request.form['password']

    web_user = webuser.validate(current_app.payment, username, password)
    if web_user is not None and web_user.is_admin():
        login_user(web_user)
        return render('placeholder.html', message="login successful!")
    return render('placeholder.html', message="login unsuccessful!")


@login.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")