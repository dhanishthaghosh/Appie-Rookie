from flask import Flask
from flask_sqlalchemy import SQLAlchemy 

app = Flask (__name__,
            instance_relative_config=False,
            template_folder="templates",
            static_folder="static")
app.config['SECRET_KEY'] = '91d54e9262c3491e8a22b74c2d0e2bca'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app) 

from booksbuddies import routes