from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskforum.config import Config


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
        from flaskforum.users.routes import users
        from flaskforum.posts.routes import posts
        from flaskforum.comments.routes import comments
        from flaskforum.main.routes import main
        from flaskforum.errors.handlers import errors
        from flaskforum.visualizations.routes import visualizations

        from flaskforum.visualizations.dash import init_dashboard
        app = init_dashboard(app)

        app.register_blueprint(users)
        app.register_blueprint(posts)
        app.register_blueprint(comments)
        app.register_blueprint(main)
        app.register_blueprint(errors)
        app.register_blueprint(visualizations)

        return app
