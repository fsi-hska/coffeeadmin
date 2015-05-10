from flask import Blueprint, render_template, abort
from flask.ext.login import login_required
from jinja2 import TemplateNotFound
from utils import *
from payment import *
import hashlib, time, random

tokens = Blueprint('tokens', __name__, template_folder='blueprints/tokens')

@tokens.route('/tokens')
@tokens.route('/tokens/')
@tokens.route('/tokens/list')
@login_required
def tokens_list():
    t = current_app.payment.session.query(Token).order_by(Token.id.desc()).all()
    return render('tokens_list.html', tokens=t)


@tokens.route('/tokens/pages/view/<string:hash>')
@login_required
def tokens_pages_view(hash):
    t = current_app.payment.session.query(Token).filter(Token.pageHash==hash).order_by(Token.id.desc()).all()
    return render('tokens_list.html', tokens=t)


@tokens.route('/tokens/pages/add', methods=['POST', 'GET'])
@login_required
def tokens_pages_add():
    if request.method == 'POST':
        try:
            value = int(request.form['value'])
        except:
            return render('tokens_pages_add.html', validation=True, value_error="Wert ist nicht int.")

        hash = hashlib.md5(str(time.time()) + str(value)).hexdigest()

        for i in range(0, 12):
            c = str(random.randint(1000000, 9999999))[:-1]
            t = Token(c, value)
            t.created_by = current_user.id
            t.creation_time = time.time()
            t.pageHash = hash
            t.valid = True
            current_app.payment.session.add(t)

        current_app.payment.session.commit()
        session['info'] = ['Yay!', 'Token-Seite hinzugefuegt!', 'success']
        return redirect('/tokens/pages/view/' + hash)
    else:
        return render('tokens_pages_add.html')