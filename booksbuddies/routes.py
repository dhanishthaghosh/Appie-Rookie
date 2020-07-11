import os
import secrets
from PIL import Image 
from flask import render_template, url_for, flash, redirect, request, abort, g
from booksbuddies import app, db, bcrypt, mail
from booksbuddies.forms import RegistrationForm, LoginForm, UpdateAccountForm, SellForm, OptionForm, RequestResetForm, ResetPasswordForm, ContactForm
from booksbuddies.models import User, Book 
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')

@app.route('/about')
def about():
    return render_template('about.html', title='About') 

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(firstname=form.firstname.data, lastname=form.lastname.data, id_num=form.id_num.data, branch=form.branch.data, mobile=form.mobile.data, username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}! From next time onwards you can login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
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

def save_picture(form_picture, folder):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/pictures/' + folder, picture_fn)

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
            picture_file = save_picture(form.picture.data, 'users')
            current_user.image_file = picture_file
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.id_num = form.id_num.data
        current_user.branch = form.branch.data 
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.mobile = form.mobile.data
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
        form.mobile.data = current_user.mobile 
    image_file = url_for('static', filename='pictures/users/' + current_user.image_file)
    return render_template('account.html', title='My Account',
                           image_file=image_file, form=form) 

@app.route('/buy', methods=['GET', 'POST']) 
def buy():
    form = OptionForm()
    page = request.args.get('page', 1, type=int) 
    if form.validate_on_submit():
        entered_sub = form.subjectbased.data if form.subjectbased.data else ''
        entered_sem = form.semesterbased.data if form.semesterbased.data else ''
        if len(entered_sub) > 0 and len(entered_sem) > 0:
            books = Book.query.filter(Book.subject.like(f'%{entered_sub}%'), Book.semester == entered_sem).paginate(page=page, per_page=2)
            return render_template('buy.html', title='Buy', form=form, books=books)
        elif len(entered_sub) > 0:
            books = Book.query.filter(Book.subject.like(f'%{entered_sub}%')).paginate(page=page, per_page=2)
            return render_template('buy.html', title='Buy', form=form, books=books)
        elif len(entered_sem) > 0:
            books = Book.query.filter(Book.semester == entered_sem).paginate(page=page, per_page=2)
            return render_template('buy.html', title='Buy', form=form, books=books)
        else:
            pass
        
    books = Book.query.paginate(page=page, per_page=2) 
    return render_template('buy.html', title='Buy', form=form, books=books)   


@app.route('/sell/new', methods=['GET', 'POST']) 
@login_required
def sell_new():
    form = SellForm()
    picture_file = None
    if form.validate_on_submit():
        if form.book_image.data: 
            picture_file = save_picture(form.book_image.data, 'books')
        book = Book(bookname=form.bookname.data, authorname=form.authorname.data, subject=form.subject.data, semester=form.semester.data, book_image=picture_file,  owner=current_user, price=form.price.data) 
        db.session.add(book)
        db.session.commit()
        flash('Your book has been uploaded!', 'success')
        return redirect(url_for('home')) 
    return render_template('sell_new.html', title='Sell New Book', form=form, 
                            legend='Upload Your Book Details') 

@app.route("/book/<int:book_id>")
@login_required
def book(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book.html', title=book.bookname, book=book)  


@app.route('/book/<int:book_id>/update', methods=['GET', 'POST'])
@login_required
def book_update(book_id):
    book = Book.query.get_or_404(book_id)
    if book.owner != current_user:
        abort(403)
    form = SellForm()
    if form.validate_on_submit():
        if form.book_image.data: 
            picture_file = save_picture(form.book_image.data, 'books')
            book.book_image = picture_file 
        book.bookname = form.bookname.data
        book.authorname = form.authorname.data
        book.subject = form.subject.data
        book.semester = form.semester.data
        book.price = form.price.data
        db.session.commit()   
        flash('Your book details has been updated.', 'success')  
        return redirect(url_for('book', book_id=book.id)) 
    elif request.method == 'GET':
        form.bookname.data = book.bookname
        form.authorname.data = book.authorname
        form.subject.data = book.subject
        form.semester.data = book.semester 
        form.book_image.data = book.book_image
        form.price.data = book.price
    book_image = url_for('static', filename='pictures/books/' + book.book_image) 
    return render_template('sell_new.html', title='Update Book Details',
                           form=form, book_image=book_image, legend='Update Your Book Details')  


@app.route("/book/<int:book_id>/delete", methods=['POST'])
@login_required
def book_delete(book_id):
    book = Book.query.get_or_404(book_id)
    if book.owner != current_user:
        abort(403)
    db.session.delete(book)
    db.session.commit()
    flash('Your book has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/user/<string:username>/books")
@login_required
def user_books(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    books = Book.query.filter_by(owner=user).paginate(page=page, per_page=2)
    return render_template('user_books.html', books=books, user=user) 


def send_reset_email(user):
    token = user.get_reset_token() 
    msg = Message('Password Reset Request', 
        sender='noreply@booksbuddies.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home')) 
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() 
        send_reset_email(user) 
        flash('An email has been sent to the above email address.', 'info')
        return redirect(url_for('login')) 
    return render_template('reset_request.html', title='Reset Password Request', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home')) 
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token.', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit() 
        flash('Your password has been updated. Now you will be able to login.', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)  
     

@app.route('/contactus', methods=['GET', 'POST'])
def contactus():
    form = ContactForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            msg = Message("Feedback", sender=app.config['MAIL_USERNAME'], recipients=[app.config['MAIL_USERNAME']])
            msg.body = f"""
            From: {form.name.data} <{form.email.data}>
            {form.body.data}
            """
            mail.send(msg)
            flash('Thanks for sending your feedback. We will reach out to you shortly.', 'success')
            return redirect(url_for('home'))
        else:
            flash('Something went wrong, please try again.', 'danger')
    return render_template('contactus.html', title='Contact', form=form) 
