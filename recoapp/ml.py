import keras
import os
import re
import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Input, Dense, Dropout, Embedding
from keras.layers import Merge, Flatten, Input, merge
from keras.optimizers import Adagrad
from scipy.stats import rankdata
from recoapp.models import Movie

MODEL_PATH = "./data/model.h5"

class CF(object):

    def __init__(self):

        user = Input(shape=(1,), name="user")
        movie = Input(shape=(1,), name="movie")

        user_vec = Embedding(input_dim=5e5, output_dim=10, name="user_vec")(user)
        movie_vec = Embedding(input_dim=5e5, output_dim=10, name="movie_vec")(movie)

        interaction = merge([user_vec, movie_vec], name="interaction", mode='dot')
        interaction = Flatten(name="flatten")(interaction)

        liked = Dense(1, activation="sigmoid", name="liked")(interaction)

        model = keras.models.Model([user, movie], liked)
        model.load_weights(MODEL_PATH)
        model.compile(loss='binary_crossentropy', optimizer='Adagrad')

        self.model = model

    def add_rating(self, user_id, movie_id, rating, passes=30):
        user_id = int(user_id)
        movie_id = int(movie_id)
        rating = int(rating)

        print "Adding rating:"
        print "User ID: %i" % user_id
        print "Movie ID: %i" % movie_id
        print "Rating ID: %i" % rating

        x = [[user_id]*passes, [movie_id] * passes]
        x = [np.array(z) for z in x]
        y = [np.array([rating]*passes)]

        self.model.fit(x, y, nb_epoch=1, batch_size=passes, verbose=0)

        return True

    def _predict(self, user_id):
        movie_ids = Movie.all_ids()
        user_ids = [user_id]*len(movie_ids)

        x = [user_ids, movie_ids]
        x = [np.array(z) for z in x]
        y = self.model.predict(x)

        return movie_ids, y


    def recommend(self, user_id, nb=5):
        ids, y = self._predict(user_id)

        print ids
        print list(y)

        return ids[top_ids], ids[bottom_ids]

    def perso(self, user_id):
        ids, y_hat = self._predict(user_id)

        y_hat = dict(zip(ids, y_hat))
        enrichment = []
        for movie in db.session.query(Movie).all():
            if movie.prob > 0 and movie.prob < 1:
                try:
                    e = y_hat[movie.id] / movie.prob
                    enrichment.append(movie.id, e)
                except KeyError:
                    print "Problem with %s" % movie.title

        top = sorted(enrichment, key=lambda x: x[1], reverse=T)
        bottom = sorted(enrichment, key=lambda x: x[1])

        top = [x[0] for x in top]
        bottom = [x[0] for x in bottom]

        return top, bottom


if __name__ == "__main__":
    cf = CF()
    cf.add_rating(1,1,True)

    print cf.recommend(1)
