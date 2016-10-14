# A movie recommendation app

This app uses Keras and Theano to implement online collaborative filtering. Users select movies that they like or dislike and the model updates the collaborative filtering model. 

## Getting started

1) Clone the repo

```
git clone https://github.com/erickramer/recoapp.git
cd recoapp
```

2) Create a virtual environment

```
virtualenv venv
source venv/bin/activate
```

3) Install python dependencies

```
pip install -r requirements.txt
```

4) Download data and build SQLite database

```
python create_db.py
```

5) Run app

```
python run_app.py
```

6) Open your browser to [localhost:50000]()

## Problems

The front-end polls the backend for new recommendations every few seconds. This probably isn't the best. Plus adding new ratings to the models takes 1-2 seconds on my macbook pro. So that delays the responsiveness of the server