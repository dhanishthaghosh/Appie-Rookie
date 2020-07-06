from booksbuddies import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) 

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    id_num = db.Column(db.String(9), unique=True, nullable=False)
    branch = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.firstname}', '{self.lastname}', '{self.id_num}', '{self.email}', '{self.username}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bookname = db.Column(db.String(100), nullable=False)
    authorname = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.bookname}', '{self.authorname}', '{self.subject}', '{self.semester}')"
