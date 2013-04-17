from flask import *
from flask.ext.login import *

def render(link, **context):
    info_title = ""
    info_message = ""
    info_type = ""

    try:
        info_title = session['info'][0]
        info_message = session['info'][1]
        info_type = session['info'][2]
        del session['info']
    except:
        pass

    return render_template(link, user=current_user, info_title=info_title, info_message=info_message, info_type=info_type, **context)