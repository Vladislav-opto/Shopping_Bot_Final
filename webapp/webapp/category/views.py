from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user, logout_user
from webapp.webapp.db_functions import create_user_choice
from webapp.webapp.model import db
from database.models import Receipt, Good
from webapp.webapp.user.models import CategoryByUser, AuthCodeByUser


blueprint = Blueprint('category', __name__)


@blueprint.route('/category', methods=['GET', 'POST'])
def index():
    try:
        authorization_code = [_.auth_code for _ in AuthCodeByUser.query.filter(AuthCodeByUser.user_id == current_user.id).order_by(AuthCodeByUser.upload.desc()).limit(1)]
    except AttributeError:
        flash('Сначала заполните форму регистрации.')
        return redirect(url_for('user.registration'))
    category_list = {_.category_name for _ in Good.query.filter(Good.receipt_id == authorization_code[0]).all()}
    if "marker" in request.form:
        if CategoryByUser.query.filter(CategoryByUser.user_id == current_user.id, CategoryByUser.receipt_id == authorization_code[0]).count():
            flash('Вы уже сделали выбор по данному чеку.')
        else:
            if Receipt.query.filter(Receipt.id == authorization_code[0]).count():
                select_category = request.form.getlist("category")
                new_user_choice = create_user_choice(select_category, current_user.email, authorization_code[0])
                if not new_user_choice:
                    flash("Выберите только 'Скидываюсь на все' или категории в отдельности.")
                    return redirect(url_for('category.index'))
                logout_user()
                flash('Ваш выбор сохранен.Вы можете вернуться к телеграм-боту.')
            else:
                flash('Введите корректный код авторизации.')
                return redirect(url_for('category.index'))
    return render_template(
        'category/index.html', categories=category_list
        )

