from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from app.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)



    with app.app_context():
        from app.users.routes import users
        from app.posts.routes import posts
        from app.comments.routes import comments
        from app.main.routes import main
        from app.errors.handlers import errors

        db.create_all()

        from dashapp.dashboard_1 import dashboard_1
        app = dashboard_1(app)
        from dashapp.dashboard_2 import dashboard_2
        app = dashboard_2(app)
        from dashapp.dashboard_3 import dashboard_3
        app = dashboard_3(app)
        from dashapp.dashboard_4 import dashboard_4
        app = dashboard_4(app)


        app.register_blueprint(users)
        app.register_blueprint(posts)
        app.register_blueprint(comments)
        app.register_blueprint(main)
        app.register_blueprint(errors)

        return app

