from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo 


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
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)],
                            render_kw={"placeholder": "Username"})
    password = PasswordField('Password', 
                            validators=[DataRequired(message='Please enter a password.')],
                            render_kw={"placeholder": "Password"})
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password', message='Passwords must match.')],
                                     render_kw={"placeholder": "Password"})
    recaptcha = RecaptchaField()
    submit = SubmitField('Make My Account')  


class LoginForm(FlaskForm):
    username = StringField('Username', 
        validators=[DataRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[DataRequired()],
        render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')  

class SellForm(FlaskForm):
    bookname = StringField('Book Name', 
        validators=[DataRequired(), Length(min=1, max=100)],
        render_kw={"placeholder": "Bookname"})
    authorname = StringField('Author/s Name', 
        validators=[DataRequired(), Length(min=1, max=100)],
        render_kw={"placeholder": "Author's name"})
    subject = StringField('Subject', 
        validators=[DataRequired()])
    semester = SelectField('Semester', validators=[DataRequired()],
        choices=[('sem1', 'Semester-I'), ('sem2', 'Semester-II'), ('sem3', 'Semester-III'), ('sem4', 'Semester-IV'), ('sem5', 'Semester-V'), ('sem6', 'Semester-VI'), ('sem7', 'Semester-VII'), ('sem8', 'Semester-VIII')])
    submit = SubmitField('Upload Book Details') 