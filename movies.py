"""
This is the people module and supports all the REST actions for the
movies data
"""

from flask import make_response, abort, jsonify
from config import db
from models import Director, Movie, MovieSchema, MovieDirectorSchema

def read_all():
    """
    This function responds to a request for /api/movies
    with the complete lists of movies
    :return:        json string of list of movies
    """
    # Create the list of movies from our data
    movies = Movie.query.order_by(Movie.id).limit(15).all()

    # Serialize the data for the response
    movie_schema = MovieSchema(many=True)
    data = movie_schema.dump(movies)
    return data

def read_one(movie_id):
    """
    This function responds to a request for /api/movies/{movie_id}
    with one matching movie from movies
    :param movie_id:   Id of movie to find
    :return:            movie matching id
    """
    # Build the initial query
    movie = (
        Movie.query.filter(Movie.id == movie_id)
        .outerjoin(Director)
        .one_or_none()
    )

    # Did we find a movie?
    if movie is not None:

        # Serialize the data for the response
        movie_schema = MovieSchema()
        data = movie_schema.dump(movie)
        return data

    # Otherwise, nope, didn't find that movie
    else:
        abort(
            status=400,
            description=f"Couldn't find movie with id {movie_id}"
        )

def read_by_name(movie_name):
    """
    This function responds to a request for /api/movies/name/{movie_name}
    with one matching movie from movies
    :param movie_name:   title of movie to find
    :return:            movie matching title
    """
    # Build the initial query
    search = "%{}%".format(movie_name)
    movie = (
        Movie.query.filter(Movie.title.like(search))
        .outerjoin(Director)
        .one_or_none()
    )

    # Did we find a movie?
    if movie is not None:
        # Serialize the data for the response
        movie_schema = MovieSchema()
        data = movie_schema.dump(movie)
        return data
    # Otherwise, nope, didn't find that movie
    else:
        abort(
            status=400,
            description=f"Couldn't find movie with title {movie_name}"
        )

def create(director_id, movie):
    """
    This function creates a new movie related to the passed in director id.
    :param director_id:       Id of the director the movie is related to
    :param movie:            The JSON containing the movie data
    :return:                201 on success
    """
    # get the parent director
    director = Director.query.filter(Director.id == director_id).one_or_none()

    # Was a director found?
    if director is None:
        abort(
            status=400,
            description=f"Couldn't find director with id {director_id}"
        )

    # Create a movie schema instance
    schema = MovieSchema()
    new_movie = schema.load(movie, session=db.session)

    # Add the movie to the director and database
    director.movies.append(new_movie)
    db.session.commit()

    # Serialize and return the newly created movie in the response
    data = schema.dump(new_movie)

    return data, 201

def read_one_details(director_id, movie_id):
    """
    This function responds to a request for
    /api/directors/{director_id}/movies/{movie_id}
    with one matching movie for the associated director
    :param director_id:       Id of director the movie is related to
    :param movie_id:         Id of the movie
    :return:                json string of movie contents
    """
    # Query the database for the movie
    movie = (
        Movie.query.join(Director, Director.id == Movie.director_id)
        .filter(Director.id == director_id)
        .filter(Movie.id == movie_id)
        .one_or_none()
    )

    # Was a movie found?
    if movie is not None:
        note_schema = MovieSchema()
        data = note_schema.dump(movie)
        return data

    # Otherwise, nope, didn't find that movie
    else:
        abort(
            status=400,
            description=f"Couldn't find movie with id {movie_id}"
        )

def update(director_id, movie_id, movie):
    """
    This function updates an existing movie related to the passed in
    director id.
    :param director_id:       Id of the director the movie is related to
    :param movie_id:         Id of the movie to update
    :param movie:            The JSON containing the movie data
    :return:                200 on success
    """
    update_movie = (
        Movie.query.filter(Director.id == director_id)
        .filter(Movie.id == movie_id)
        .one_or_none()
    )

    # Did we find an existing movie?
    if update_movie is not None:

        # turn the passed in movie into a db object
        schema = MovieSchema()
        update = schema.load(movie, session=db.session)

        # Set the id's to the movie we want to update
        update.director_id = update_movie.director_id
        update.id = update_movie.id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated movie in the response
        data = schema.dump(update_movie)

        return data, 200

    # Otherwise, nope, didn't find that movie
    else:
        abort(
            status=400,
            description=f"Couldn't find movie with id {movie_id}"
        )

def delete(director_id, movie_id):
    """
    This function deletes a movie from the movie structure
    :param director_id:   Id of the director the movie is related to
    :param movie_id:     Id of the movie to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the movie requested
    movie = (
        Movie.query.filter(Director.id == director_id)
        .filter(Movie.id == movie_id)
        .one_or_none()
    )

    # did we find a movie?
    if movie is not None:
        db.session.delete(movie)
        db.session.commit()
        # return make_response(
        #     "Movie {movie_id} deleted".format(movie_id=movie_id), 200
        # )
        return make_response(
            jsonify(
                {
                    "message": "Movie {movie_id} deleted"
                }
            ),
            200
        )
    # Otherwise, nope, didn't find that movie
    else:
        abort(
            status=400,
            description=f"Couldn't find movie with id {movie_id}"
        )