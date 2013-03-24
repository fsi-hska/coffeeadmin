#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
sys.path.insert(0, "coffeeserver/")
import coffeeserver

app = Flask(__name__)
Bootstrap(app)
app.config['BOOTSTRAP_USE_CDN'] = True
app.config['BOOTSTRAP_FONTAWESOME'] = True

p = coffeeserver.load_payment()

@app.route('/')
def index():
    p.getItems()
    return render_template('test.html')


@app.route('/breakme/')
def breakme():
    return render_template('test.html')

if __name__ == '__main__':
    app.run(debug=True)