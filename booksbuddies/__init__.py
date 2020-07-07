from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager

app = Flask (__name__,
            instance_relative_config=False,
            template_folder="templates",
            static_folder="static")
app.config['SECRET_KEY'] = '91d54e9262c3491e8a22b74c2d0e2bca'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app) 
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'warning'

from booksbuddies import routes 