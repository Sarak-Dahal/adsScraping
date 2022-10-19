# __init__ will bring our application together
from flask_bootstrap import Bootstrap
from flask import Flask

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = 'nei349h(*!@HF#FF'
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Using bootstrap
bootstrap = Bootstrap(app)

from app import user
