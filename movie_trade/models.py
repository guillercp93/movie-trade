from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class BaseModel(db.Model):
    """Base data model for all objects"""
    __abstract__ = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        """Define a base way to print models"""
        return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in self._to_dict().items()
        })

    def json(self):
        """
                Define a base way to jsonify models, dealing with datetime objects
        """
        return {
            column: value if not isinstance(value, datetime.date) else value.strftime('%Y-%m-%d')
            for column, value in self._to_dict().items()
        }


class Movies(BaseModel, db.Model):
    """Model for the movies table"""
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key = True)
    code = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    genre = db.Column(db.String(30), nullable=False)

class ImagesMovie(BaseModel, db.Model):
    """Model for the images table of movies registered"""
    __tablename__ = 'imagesmovies'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(80), unique=True)
    route = db.Column(db.Text)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'),
        nullable=False)
    movie = db.relationship('Movies',
        backref=db.backref('imagesmovies', lazy=True))