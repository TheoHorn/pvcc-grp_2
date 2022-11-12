from flask import render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user, logout_user, login_user

from . import app
from ..model.database.entity.user import User
from ..setup_sql import db


@app.get('/')
def home():
    return render_template('home.html')


@app.get('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@app.get('/signup')
def signup():
    callback = request.args.get('next')
    if callback is None:
        callback = ''
    else:
        callback = "?next=" + callback
    return render_template('signup.html', callback=callback)


@app.post('/signup')
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()
    callback = request.args.get('next')

    if user:
        flash('L\'email existe déjà')
        return redirect(url_for('controller.signup', next=callback))

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('controller.login', next=callback))


@app.get('/login')
def login():
    callback = request.args.get('next')
    if callback is None:
        callback = ''
    else:
        callback = "?next=" + callback
    return render_template('login.html', callback=callback)


@app.post('/login')
def login_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()
    callback = request.args.get('next')

    if not user:
        flash('Email inconnu')
        return redirect(url_for('controller.login', next=callback))
    if not check_password_hash(user.password, password):
        flash('Mot de passe incorrect')
        return redirect(url_for('controller.login', next=callback))

    login_user(user)

    if callback is not None:
        return redirect(callback)

    return redirect(url_for('controller.profile'))


@app.get('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('controller.login'))
