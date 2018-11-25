## Create migrations
python manage.py db init
python manage.py db migrate
python manage.py db upgrade

## Run application
python manage.py runserver

## Environment variables
SQLALCHEMY_DATABASE_URI = path/to/database
FLASK_APP=movie_trade
FLASK_ENV=development||production
UPLOAD_FOLDER = path/to/uploaded/files