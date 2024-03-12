from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models import User, Plan  
from app.extensions import app, db, bcrypt

class SignUpForm(FlaskForm):
    username = StringField('Username',
            vaildators = [DataRequired(), Length(min=3, max=50)])
    password = StringField('Password', validators=[DataRequired()])
    name = StringField('Your name', validators = [DataRequired()])
    plan = SelectField('Which plan would you like to use', choices=Plan.choices())
    savings = FloatField('How much do you currently have saved', validators=[DataRequired()])
    submit = SubmitField('Start Saving!')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError
        ('This username is already taken. Please log in or choose a different one.')
        
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError('No user with that username. Please try again.')
    
    def validate_password(self, password):
        user = User.query.filter_by(username = self.username.data).first()
        if user and not bcrypt.check_password_hash(
                user.password, password.data):
            raise ValidationError('Password doesn\'t match. Please try again')