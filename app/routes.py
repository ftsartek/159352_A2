from flask import render_template, request, escape, abort, session, redirect
from app import app, database, forms
from passlib.hash import sha512_crypt

app.secret_key = 'v98Hwg93nBA5sv-0238tVNsk2d='
app.config['SESSION_TYPE'] = 'filesystem'


@app.route('/')
def index():
    return render_template("index.jinja")


@app.route('/routes')
def routes():
    return render_template("routes.jinja")


@app.route('/login', methods=['GET', 'POST'])
def login():
    pass