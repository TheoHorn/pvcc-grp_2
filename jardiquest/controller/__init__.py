from flask import Blueprint

# allow to create path in multiple file
app = Blueprint('controller', __name__)

# to create a new file of path import him here
# please ignore the 'PEP 8: E402' warning ( create an import partial if you move them to the top file )
from .sample import *
