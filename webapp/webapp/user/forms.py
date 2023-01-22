from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

class UserForm(FlaskForm):
    first_name = StringField('Имя', validators=[DataRequired()], render_kw={'class': 'form-control'})
    last_name = StringField('Фамилия', validators=[DataRequired()], render_kw={'class': 'form-control'})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'class': 'form-control'})
    submit = SubmitField('Отправить', render_kw={'class': 'btn btn-primary'})
