from flask import Flask
from flask_login import LoginManager
from webapp.webapp.model import db
from webapp.webapp.user.models import AuthWebApp
from webapp.webapp.user.views import blueprint as user_blueprint
from webapp.webapp.category.views import blueprint as category_blueprint
from settings_box import settings

def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'
    app.register_blueprint(user_blueprint)
    app.register_blueprint(category_blueprint)


    @login_manager.user_loader
    def load_user(user_id):
        return AuthWebApp.query.get(user_id)

    return app
