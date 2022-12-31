from http.client import HTTPException

from flask import request,render_template, flash, redirect, url_for
from flask_login import current_user

from jardiquest.controller import handling_status_error
from jardiquest.model.database.entity.user import User
from jardiquest.model.database.entity.jardin import Jardin

from jardiquest.setup_sql import db

def render_home():
    return render_template('blog.html',user=current_user)