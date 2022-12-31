from flask import render_template
from flask_login import current_user, login_required

from jardiquest.controller import app


@app.get('/blog')
def blog():
    from jardiquest.model.path.blog_model import render_home
    return render_home()


