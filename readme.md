Flask Forum Project:

Steps to start new database via sqlalchemy. Enter the following through python console:

 - from flaskforum import create_app
 - app = create_app()
 - app.app_context().push()
 - from flaskforum import db
 - db.drop_all()
 - db.create_all()

Parameters to be stored in flask_forum/flaskforum/.env:

 - SECRET_KEY =
 - SQLALCHEMY_DATABASE_URI =
 - FLASK_ENV=