from recoapp import app, db
from flask import render_template, jsonify
from recoapp.models import Movie
from flask import request
from ml import CF
import numpy as np

# initialize Keras model
cf = CF()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/movies')
def movies():
    movies = db.session.query(Movie).all()
    np.random.shuffle(movies)
    movies = [m.to_dict() for m in movies]
    return jsonify(movies)

@app.route('/api/recommend/<int:user_id>')
def recommend(user_id):

    def get_movies(ids):
        ids = list(ids)
        q = db.session.query(Movie)
        movies = q.filter(Movie.id.in_(ids)).all()
        return [m.to_dict() for m in movies]

    top, bottom = cf.recommend(user_id)
    top_movies = get_movies(top)
    bottom_movies = get_movies(bottom)

    d = {"top": top_movies, "bottom": bottom_movies}
    return jsonify(d)

@app.route('/api/perso/<int:user_id>')
def perso(user_id):

    def get_movies(ids):
        ids = list(ids)
        q = db.session.query(Movie)
        movies = q.filter(Movie.id.in_(ids)).all()
        return [m.to_dict() for m in movies]

    top, bottom = cf.perso(user_id)
    print top
    print bottom
    top_movies = get_movies(top)
    bottom_movies = get_movies(bottom)

    d = {"top": top_movies, "bottom": bottom_movies}
    return jsonify(d)



@app.route('/api/rate', methods=["POST"])
def rate():
    d = request.form
    cf.add_rating(d['user_id'], d['movie_id'], d['liked'])
    return jsonify(True)

@app.route('/static/<path:path>')
def static_file(path):
    return app.send_static_file(path)
