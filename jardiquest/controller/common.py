from flask import render_template
from flask_login import current_user, login_required

from jardiquest.controller import app


@app.get('/')
def home():
    return render_template('home.html')


@app.get('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

