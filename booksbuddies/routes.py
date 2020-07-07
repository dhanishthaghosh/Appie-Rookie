import os
import secrets
from PIL import Image 
from flask import render_template, url_for, flash, redirect, request 
from booksbuddies import app, db, bcrypt
from booksbuddies.forms import RegistrationForm, LoginForm, UpdateAccountForm
from booksbuddies.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')

@app.route('/about')
def about():
    return render_template('about.html', title='About') 

@app.route("/register", methods=['GET', 'POST'])
def register():
    # print('Entered register method')
    form = RegistrationForm()
    print('Entered register method')
    if form.validate_on_submit():
        # print("Registration Data submitted")
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(firstname=form.firstname.data, lastname=form.lastname.data, id_num=form.id_num.data, branch=form.branch.data, username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        # print(firstname, lastname, id_num, branch, username, email) 
        flash('Account created for {form.username.data}! From next time onwards you can login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    print('Login method')
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home')) 
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home')) 

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/pictures', picture_fn)

    output_size = (130, 130)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.id_num = form.id_num.data
        current_user.branch = form.branch.data 
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been successfully updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.id_num.data = current_user.id_num
        form.branch.data = current_user.branch
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='pictures/' + current_user.image_file)
    return render_template('account.html', title='My Account',
                           image_file=image_file, form=form) 

@app.route('/buy') 
def buy():
    return render_template('buy.html', title='Buy')   

@app.route('/buy/based on subject')
def buy2_1():
    return render_template('buy2_1.html', title='Buy | Based on Subject') 

@app.route('/sell', methods=['GET', 'POST']) 
@login_required
def sell():
    return render_template('sell.html', title='Sell') 