from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from sqlalchemy.orm import relationship



app = Flask(__name__)

app.config['SECRET_KEY'] = 'fad7f2dd2d33c0a90d44c3c3b8cf122f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
from flaskBlog import routes