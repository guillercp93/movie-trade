import os
from dotenv import load_dotenv
from flask import Flask, send_from_directory
from .models import db
from .views import bp
from werkzeug.utils import secure_filename

load_dotenv(verbose=True)

def create_app(test_config=None):
    # create and configure app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI'),
        UPLOAD_FOLDER=os.getenv('UPLOAD_FOLDER', os.path.join(app.instance_path, 'media'))
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
        os.makedirs(os.path.join(app.instance_path, 'media'))
    except OSError:
        pass


    @app.route('/uploads/<filename>')
    def download_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    db.init_app(app)

    app.register_blueprint(bp)
    app.add_url_rule('/', endpoint="index")

    return app