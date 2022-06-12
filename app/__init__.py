from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# FOLDER_FOR_FILES = '/uploads'
# ALLOWED_FILES = set(['xlsx', 'xlsm', 'xltx', 'xltm'])

app = Flask(__name__)
app.config.from_object(Config)
# app.config['FOLDER_FOR_FILES'] = FOLDER_FOR_FILES
# app.config['ALLOWED_FILES'] = ALLOWED_FILES
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = "signin"

from app import routes, models
