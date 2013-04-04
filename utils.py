from flask import *
from flask.ext.login import *

def render(link, **context):
    return render_template(link, user=current_user, **context)