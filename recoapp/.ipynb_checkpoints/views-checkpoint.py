from recoapp import app, db
from flask import render_template, jsonify
from recoapp.models import Movie

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/movies')
def movies():
    movies = db.session.query(Movie).all()
    movies = [m.to_dict() for m in movies]
    return jsonify(movies[0:5])

@app.route('/static/<path:path>')
def static_file(path):
    return app.send_static_file(path)