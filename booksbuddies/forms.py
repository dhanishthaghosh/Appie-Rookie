from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from booksbuddies.models import User


class RegistrationForm(FlaskForm):
    firstname = StringField('First Name',
                           validators=[DataRequired(), Length(min=1, max=20)], 
                           render_kw={"placeholder": "Harry"})
    lastname = StringField('Last Name',
                        validators=[DataRequired(), Length(min=1, max=20)],
                        render_kw={"placeholder": "Potter"})
    id_num = StringField('Identity Number',
                            validators=[DataRequired(), Length(min=9, max=9)],
                            render_kw={"placeholder": "19108100"})
    branch = SelectField('Branch Name', 
                        choices=[('none', 'None'), ('civil', 'Civil Enginnering'), ('comps', 'Computer Science'), ('elec', 'Electrical Engineering'), ('tronic', 'Electronics Engineering'), ('extc', 'Electronics and Telecommunication Enginnering'), ('it', 'Information Technology'), ('mech', 'Mechanical Engineering'), ('prod', 'Production Engineering'), ('text', 'Textile Engineering')])
    email = StringField('Email',
                        validators=[DataRequired(), Email(message='Please enter a valid email address.')], render_kw={"placeholder": "harrypotter@gmail.com"}) 
    username = StringField('Create an Username', 
                            validators=[DataRequired(), Length(min=4, max=20)],
                            render_kw={"placeholder": "Username"})
    password = PasswordField('Create a Password', 
                            validators=[DataRequired(message='Please enter a password.')],
                            render_kw={"placeholder": "Password"})
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password', message='Passwords must match.')],
                                     render_kw={"placeholder": "Password"})
    # recaptcha = RecaptchaField()
    submit = SubmitField('Make My Account')  

    def validate_id_num(self, id_num):
        user = User.query.filter_by(id_num=id_num.data).first()
        if user:
            raise ValidationError('This id_num already belongs to someone else. Please try again with your own identity number.')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is taken. Please try another one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is taken. Please try another one.')


class LoginForm(FlaskForm):
    username = StringField('Username', 
        validators=[DataRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[DataRequired()],
        render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')  


class SellForm(FlaskForm):
    bookname = StringField('Book Name', 
        validators=[DataRequired(), Length(min=1, max=150)],
        render_kw={"placeholder": "Bookname"})
    authorname = StringField('Author/s Name', 
        validators=[DataRequired(), Length(min=1, max=150)],
        render_kw={"placeholder": "Author's name"})
    subject = StringField('Subject', validators=[DataRequired(), Length(min=1, max=150)],
        render_kw={"placeholder": "Subject"})
    semester = SelectField('Semester', validators=[DataRequired()],
        choices=[('sem1', 'Semester-I'), ('sem2', 'Semester-II'), ('sem3', 'Semester-III'), ('sem4', 'Semester-IV'), ('sem5', 'Semester-V'), ('sem6', 'Semester-VI'), ('sem7', 'Semester-VII'), ('sem8', 'Semester-VIII')]) 
    submit = SubmitField('Upload Book Details') 


class UpdateAccountForm(FlaskForm):
    firstname = StringField('First Name',
                           validators=[DataRequired(), Length(min=1, max=20)])
    lastname = StringField('Last Name',
                           validators=[DataRequired(), Length(min=1, max=20)])
    id_num = StringField('Identity Number',
                            validators=[DataRequired(), Length(min=9, max=9)])
    branch = SelectField('Branch Name', 
                        choices=[('none', 'None'), ('civil', 'Civil Enginnering'), ('comps', 'Computer Science'), ('elec', 'Electrical Engineering'), ('tronic', 'Electronics Engineering'), ('extc', 'Electronics and Telecommunication Enginnering'), ('it', 'Information Technology'), ('mech', 'Mechanical Engineering'), ('prod', 'Production Engineering'), ('text', 'Textile Engineering')])
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update Information')

    def validate_id_num(self, id_num):
        if id_num.data != current_user.id_num:
            user = User.query.filter_by(id_num=id_num.data).first()
            if user:
                raise ValidationError('This ID number is alreedy in use. Please choose a different one.')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This email is taken. Please choose a different one.')


class OptionForm(FlaskForm):
    subjectbased = StringField('Based On Subject', 
            validators=[DataRequired(), Length(min=1, max=100)],
            render_kw={"placeholder": "Subject"})
    semesterbased = SelectField('Based On Semester', 
            validators=[DataRequired()], choices=[('sem1', 'Semester-I'), ('sem2', 'Semester-II'), ('sem3', 'Semester-III'), ('sem4', 'Semester-IV'), ('sem5', 'Semester-V'), ('sem6', 'Semester-VI'), ('sem7', 'Semester-VII'), ('sem8', 'Semester-VIII')])
    submit = SubmitField('Show Results') 
    