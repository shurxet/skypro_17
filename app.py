# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


api = Api(app)
api.app.config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 4}

movies_ns = api.namespace('movies')
directors_ns = api.namespace('directors')
genres_ns = api.namespace('genres')


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")

class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()


class DirectorSchema(Schema):
    id = fields.Int()
    name = fields.Str()


class GenreSchema(Schema):
    id = fields.Int()
    name = fields.Str()


movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


@movies_ns.route('/')
class MoviesView(Resource):
    def get(self):
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')

        movies = Movie.query

        if director_id:
            movies = movies.filter(Movie.director_id == director_id)
        if genre_id:
            movies = movies.filter(Movie.genre_id == genre_id)
        movies = movies.all()

        return movies_schema.dump(movies), 200

    def post(self):
        req_json = request.json
        new_movie = Movie(**req_json)

        with db.session.begin():
            db.session.add(new_movie)
            db.session.commit()

        return "", 201


@movies_ns.route('/<int:mid>')
class MovieView(Resource):
    def get(self, mid: int):
        try:
            movie = Movie.query.get(mid)
            return  movie_schema.dump(movie), 200
        except Exception as e:
            return str(e), 404

    def put(self, mid: int):
        movie = Movie.query.get(mid)
        req_json = request.json

        movie.title = req_json.get("title")
        movie.description = req_json.get("description")
        movie.trailer = req_json.get("trailer")
        movie.year = req_json.get("year")
        movie.rating = req_json.get("rating")
        movie.genre_id = req_json.get("genre_id")
        movie.director_id = req_json.get("director_id")

        db.session.add(movie)
        db.session.commit()

        return "", 201

    def patch(self, mid: int): # Частичное обновление
        movie = Movie.query.get(mid)
        req_json = request.json

        if "title" in req_json:
            movie.id  = req_json.get("title")

        if "description" in req_json:
            movie.description = req_json.get("description")

        if "trailer" in req_json:
            movie.description = req_json.get("trailer")

        if "year" in req_json:
            movie.year = req_json.get("year")

        db.session.add(movie)
        db.session.commit()

    def delete(self, mid: int):
        movie = Movie.query.get(mid)

        db.session.delete(movie)
        db.session.commit()

        return "", 204


@directors_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        director = Director.query.all()

        return directors_schema.dump(director), 200

    def post(self):
        req_json = request.json
        new_director = Director(**req_json)

        with db.session.begin():
            db.session.add(new_director)
            db.session.commit()

        return "", 201


@directors_ns.route('/<int:did>')
class DirectorView(Resource):
    def get(self, did: int):
        try:
            director = Director.query.get(did)
            return  director_schema.dump(director), 200
        except Exception as e:
            return str(e), 404

    def put(self, did: int):
        director = Director.query.get(did)
        req_json = request.json

        director.name = req_json.get("name")

        db.session.add(director)
        db.session.commit()

        return "", 201

    def patch(self, did: int): # Частичное обновление
        director = Director.query.get(did)
        req_json = request.json

        if "name" in req_json:
            director.name = req_json.get("name")

        db.session.add(director)
        db.session.commit()

    def delete(self, did: int):
        director = Director.query.get(did)

        db.session.delete(director)
        db.session.commit()

        return "", 204


@genres_ns.route('/')
class GenresView(Resource):
    def get(self):
        genre = Genre.query.all()

        return genres_schema.dump(genre), 200

    def post(self):
        req_json = request.json
        new_genre = Genre(**req_json)

        with db.session.begin():
            db.session.add(new_genre)
            db.session.commit()

        return "", 201


@genres_ns.route('/<int:gid>')
class GenreView(Resource):
    def get(self, gid: int):
        try:
            genre = Genre.query.get(gid)
            return genre_schema.dump(genre), 200
        except Exception as e:
            return str(e), 404

    def put(self, gid: int):
        genre = Genre.query.get(gid)
        req_json = request.json

        genre.name = req_json.get("name")

        db.session.add(genre)
        db.session.commit()

        return "", 201

    def patch(self, gid: int):  # Частичное обновление
        genre = Genre.query.get(gid)
        req_json = request.json

        if "name" in req_json:
            genre.name = req_json.get("name")

        db.session.add(genre)
        db.session.commit()

    def delete(self, gid: int):
        genre = Genre.query.get(gid)

        db.session.delete(genre)
        db.session.commit()

        return "", 204


if __name__ == '__main__':
    app.run(debug=True)
