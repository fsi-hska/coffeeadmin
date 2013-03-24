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
    return render_template('home.html')

@app.route('/items/')
def items():
    print p.getItems()
    return render_template('items.html', items=p.getItems())

@app.route('/transactions/')
def transactions():
    return render_template('placeholder.html')

@app.route('/contact/')
def contact():
    return render_template('placeholder.html')

if __name__ == '__main__':
    app.run(debug=True)