from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField, FileField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_wtf.file import FileAllowed

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class AddPlantForm(FlaskForm):
    nickname = StringField('Plant nickname', validators=[DataRequired()])
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    last_watering = DateField('Last watering date', format='%Y-%m-%d', validators=[DataRequired()])
    photo = FileField('Upload photo', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Add Plant')

class AddCategoryForm(FlaskForm):
    name = StringField('Plant Name', validators=[DataRequired()])
    latin_name = StringField('Latin Name')
    watering_interval = StringField('Watering Interval (days)', validators=[DataRequired()])
    submit = SubmitField('Add Category')





