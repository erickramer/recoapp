from recoapp import app, db
import recoapp.models
import pandas as pd
import re
import urllib
import zipfile

def extract_year(x):
    year = re.search("[12][0-9][0-9][0-9]", x)

    if year:
        title = re.sub("[ \t]+\(.+\)", "", x)
        return title, year.group(0)

    return x, None

## Download movieles data

print "Downloading MovieLens data"

urlopener = urllib.URLopener()
urlopener.retrieve('http://files.grouplens.org/datasets/movielens/ml-20m.zip', './data/ml-20m.zip')

zip_ref = zipfile.ZipFile('./data/ml-20m.zip', 'r')
zip_ref.extractall('./data/')
zip_ref.close()

## Input into database

movies = pd.read_csv("./data/ml-20m/movies.csv", index_col='movieId')
ratings = pd.read_csv("./data/ml-20m/ratings.csv")

ratings['liked'] = ratings.rating > 3.5

avg_rating = ratings.groupby(['movieId']).mean()
avg_rating = avg_rating[['liked']]

movies = movies.join(avg_rating)
movies = movies[['title', 'liked']]

db.drop_all()
db.create_all()

for movie_id, x, liked in movies.itertuples():

    title, year = extract_year(x)

    movie = recoapp.models.Movie(movie_id, title, year, liked)

    try:
        db.session.add(movie)
        db.session.commit()
    except:
        print "A problem with: ",
        print movie
        db.session.rollback()

    if movie_id % 100 == 0:
        print "%i movies added to database" % movie_id
