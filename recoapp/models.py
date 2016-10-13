from recoapp import app, db

class Movie(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(150))
    year = db.Column(db.Integer)
    rating = db.Column(db.Numeric)

    def __init__(self, id, title, year, prob):
        self.id = int(id)
        self.title = title.decode('UTF-8')
        self.prob = prob

        if year is not None:
            self.year = int(year)

    def __repr__(self):
        return '<Movie %r>' % self.title

    def to_dict(self):
        return {'id': self.id, 'title': self.title, 'year': self.year}

    @classmethod
    def all_ids(cls):
        ids = db.session.query(Movie.id).all()
        return [i[0] for i in ids]
