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

    def raw_prob(m):
        try:
            return m['prob_predicted']
        except KeyError:
            return 0

    def normed_prob(m):
        try:
            if m['prob'] > 0 and m['prob'] < 1:
                return m['prob_predicted'] / m['prob']
        except KeyError:
            pass
        return 0

    key = raw_prob if request.args['method'] == 'raw' else normed_prob
    y = cf.recommend(user_id)

    movies = db.session.query(Movie).all()
    movies = {m.id: m.to_dict() for m in movies}
    for movie_id, prob in y:
        try:
            movies[movie_id]['prob_predicted'] = prob
        except KeyError:
            pass

    movies = movies.values()
    movies = sorted(movies, key=key)
    d = {'bottom': movies[0:5], 'top': movies[::-1][0:5]}

    return jsonify(d)



@app.route('/api/rate', methods=["POST"])
def rate():
    d = request.form
    cf.add_rating(d['user_id'], d['movie_id'], d['liked'])
    return jsonify(True)

@app.route('/static/<path:path>')
def static_file(path):
    return app.send_static_file(path)
