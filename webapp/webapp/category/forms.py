from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

class CodeForm(FlaskForm):
    authorization_code = StringField('Код авторизации', validators=[DataRequired()], render_kw={'class': 'form-control'})
