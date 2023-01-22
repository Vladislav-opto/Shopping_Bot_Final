from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user, logout_user
from webapp.webapp.db_functions import create_user_choice
from database.models import Category, Receipt
from webapp.webapp.category.forms import CodeForm
from webapp.webapp.user.models import CategoryByUser


blueprint = Blueprint('category', __name__)


@blueprint.route('/category', methods=['GET', 'POST'])
def index():
    form=CodeForm()
    category_list = Category.query.all()
    authorization_code = form.authorization_code.data
    if "marker" in request.form:
        if CategoryByUser.query.filter(CategoryByUser.user_id == current_user.id, CategoryByUser.receipt_id == authorization_code).count():
            flash('Вы уже сделали выбор по данному чеку.')
        else:
            if Receipt.query.filter(Receipt.id == authorization_code).count():
                select_category = request.form.getlist("category")
                try:
                    new_user_choice = create_user_choice(select_category, current_user.email, authorization_code)
                    if not new_user_choice:
                        flash("Выберите только 'Скидываюсь на все' или категории в отдельности.")
                        return redirect(url_for('category.index'))
                    logout_user()
                    flash('Ваш выбор сохранен.Вы можете вернуться к телеграм-боту.')
                except AttributeError:
                    flash('Сначала заполните форму регистрации.')
                    return redirect(url_for('user.registration'))
            else:
                flash('Введите корректный код авторизации.')
                return redirect(url_for('category.index'))
    return render_template(
        'category/index.html', categories=category_list, form=form
        )

