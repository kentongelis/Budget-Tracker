from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, SubmitField, TextAreaField, FloatField, widgets
from wtforms.validators import DataRequired, Length
from app.models import Plan

class PostForm(FlaskForm):
    data = TextAreaField('Write your tips here!', validators=[DataRequired(), Length(min=1)])
    submit = SubmitField('Post!')
    
class PaycheckForm(FlaskForm):
    amount = FloatField('How much did you make on your last paycheck?', validators=[DataRequired()])
    submit = SubmitField('Enter')
    
class UpdatePlanForm(FlaskForm):
    new_plan = SelectField('Select your new plan!', choices=Plan.choices(), validators=[DataRequired()])
    submit = SubmitField('Update')
    
class CategoryForm(FlaskForm):
    title = StringField('Title of the category', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
class AIForm(FlaskForm):
    question = TextAreaField('Enter your question', validators=[DataRequired(), Length(min=1)])
    submit = SubmitField('Submit')