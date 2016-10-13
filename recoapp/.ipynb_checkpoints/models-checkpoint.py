from recoapp import app, db

class Movie(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(150))
    year = db.Column(db.Integer)

    def __init__(self, id, title, year):
        self.id = int(id)
        self.title = title.decode('UTF-8')
        
        if year is not None:
            self.year = int(year)
        
    def __repr__(self):
        return '<Movie %r>' % self.title
    
    def to_dict(self):
        return {'id': self.id, 'title': self.title, 'year': self.year}