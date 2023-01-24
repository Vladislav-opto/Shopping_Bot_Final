from flask import Blueprint, render_template, url_for, flash, redirect
from flask_login import login_user

from sqlalchemy.exc import IntegrityError

from webapp.webapp.db_functions import create_user, create_auth_code_by_id
from webapp.webapp.user.forms import UserForm
from webapp.webapp.user.models import AuthWebApp


blueprint = Blueprint('user', __name__)


@blueprint.route('/')
def registration():
    registration_form = UserForm()
    return render_template('user/registration.html', form=registration_form)


@blueprint.route('/process-registration', methods=['POST'])
def process_registration():
    form = UserForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        authorization_code = form.authorization_code.data
        if AuthWebApp.query.filter(AuthWebApp.first_name == first_name, AuthWebApp.last_name == last_name, AuthWebApp.email == email).count():
            user = AuthWebApp.query.filter_by(email=email).first()
            create_auth_code_by_id(authorization_code, user.id)
            login_user(user)
            return redirect(url_for('category.index'))
        else:
            try:
                create_user(first_name,last_name, email)
                user = AuthWebApp.query.filter_by(email=email).first()
                create_auth_code_by_id(authorization_code, user.id)
                login_user(user)
            except IntegrityError:
                flash('Пользователь с таким email уже существует.')
                return redirect(url_for('user.registration'))
            return redirect(url_for('category.index'))
    flash('Введите корректную почту.')
    return redirect(url_for('user.registration'))
