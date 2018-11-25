from flask import Blueprint, current_app as app, redirect, render_template, request
from .models import Movies, ImagesMovie, db
from werkzeug.utils import secure_filename
import os

bp = Blueprint('movies', __name__)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'pgm', 'bmp'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/')
def index ():
    result = db.engine.execute("""
        SELECT
            m.id,
            m.code,
            m.name,
            m.description,
            m.genre,
            min(i.filename) AS filename
        FROM
            movies AS m
        RIGHT JOIN imagesmovies AS i ON
            i.movie_id = m.id
        GROUP BY
            m.id,
            m.code,
            m.name,
            m.genre,
            m.description;
        """)
    return render_template('movies.html', movies=result)

@bp.route('/movies/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        code = request.form.get('code')
        if not code:
            return render_template('create_movie.html', error="Empty code field")
        name = request.form.get('name')
        if not name:
            return render_template('create_movie.html', error="Empty name field")
        description = request.form.get('description')
        if not description:
            return render_template('create_movie.html', error="Empty description field")
        genre = request.form.get('genre')
        if not genre:
            return render_template('create_movie.html', error="Empty genre field")
        
        new_movie = Movies()
        new_movie.code = code
        new_movie.name = name
        new_movie.description = description
        new_movie.genre = genre

        db.session.add(new_movie)
        db.session.commit()

        return redirect('/movies/detail/%d/' % new_movie.id)
    
    return render_template('create_movie.html')

@bp.route('/movies/edit/<int:movie_id>/', methods=('GET', 'POST'))
def edit(movie_id):
    movie = Movies.query.filter_by(id=movie_id).first()
    if request.method == 'POST':
        code = request.form.get('code')
        if not code:
            return render_template('edit_movie.html', error="Empty code field")
        name = request.form.get('name')
        if not name:
            return render_template('edit_movie.html', error="Empty name field")
        description = request.form.get('description')
        if not description:
            return render_template('edit_movie.html', error="Empty description field")
        genre = request.form.get('genre')
        if not genre:
            return render_template('edit_movie.html', error="Empty genre field")
        
        movie.code = code
        movie.name = name
        movie.description = description
        movie.genre = genre

        db.session.add(movie)
        db.session.commit()

        return redirect('/movies/detail/%d/' % movie.id)
    
    return render_template('edit_movie.html', movie=movie)

@bp.route('/movies/detail/<int:movie_id>/')
def movie_detail(movie_id):
    movie = Movies.query.filter_by(id=movie_id).first_or_404()
    images = ImagesMovie.query.filter_by(movie_id=movie_id)
    db.session.commit()
    return render_template('detail_movie.html', movie=movie, images=images)

@bp.route('/images/', methods=('GET', 'POST'))
def upload_images():
    movies = Movies.query.order_by('id').all()
    movies = [{"id": m.id, "name":m.name, "code": m.code} for m in movies]

    if request.method == 'POST':
        movie_id = request.form['movie_id']
        if not movie_id:
            return render_template('upload_images.html', movies=movies, error="Not selected movie")
        file = request.files['image']
        if file.filename == '':
            return render_template('upload_images.html', movies=movies, error="Not selected image")
        if file and not allowed_file(file.filename):
            return render_template('upload_images.html', movies=movies, error="Incorrect file's format")
        filename = secure_filename(file.filename)
        if len(filename) > 80:
            return render_template('upload_images.html', movies=movies, error="Filename too large. Max 80 characters")
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        movie = Movies.query.get(movie_id)
        image = ImagesMovie()
        image.filename = filename
        image.route = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.movie = movie
        
        db.session.add(image)
        db.session.commit()

        return redirect('/movies/detail/%s/' % movie_id)

    return render_template('upload_images.html', movies=movies)