"""
This is the people module and supports all the REST actions for the
directors data
"""

from flask import make_response, abort
from config import db
from models import Director, Movie, DirectorSchema, DirectorMovieSchema

def read_all():
    """
    This function responds to a request for /api/people
    with the complete lists of people
    :return:        json string of list of people
    """
    # Create the list of people from our data
    directors = Director.query.order_by(Director.id).all()

    # Serialize the data for the response
    director_schema = DirectorSchema(many=True)
    data = director_schema.dump(directors)
    return data
    
def read_one(director_id):
    """
    This function responds to a request for /api/people/{director_id}
    with one matching person from people
    :param director_id:   Id of person to find
    :return:            person matching id
    """
    # Build the initial query
    director = (
        Director.query.filter(Director.id == director_id)
        .outerjoin(Movie)
        .one_or_none()
    )

    # Did we find a director?
    if director is not None:

        # Serialize the data for the response
        movie_schema = DirectorSchema()
        data = movie_schema.dump(director)
        return data

    # Otherwise, nope, didn't find that person
    else:
        abort(404, f"Person not found for Id: {director_id}")

def create(director):
    """
    This function creates a new director in the people structure
    based on the passed in director data
    :param director:  director to create in people structure
    :return:        201 on success, 406 on director exists
    """
    name = director.get("name")

    existing_director = (
        Director.query.filter(Director.name == name)
        .one_or_none()
    )

    # Can we insert this director?
    if existing_director is None:

        # Create a director instance using the schema and the passed in director
        schema = DirectorSchema()
        new_director = schema.load(director, session=db.session)

        # Add the director to the database
        db.session.add(new_director)
        db.session.commit()

        # Serialize and return the newly created person in the response
        data = schema.dump(new_director)

        return data, 201

    # Otherwise, nope, person exists already
    else:
        abort(409, f"Director with name {name} already exist")

def update(director_id, director):
    """
    This function updates an existing director in the people structure
    :param director_id:   Id of the director to update in the people structure
    :param director:      director to update
    :return:            updated director structure
    """
    # Get the director requested from the db into session
    update_director = Director.query.filter(
        Director.id == director_id
    ).one_or_none()

    # Did we find an existing director?
    if update_director is not None:

        # turn the passed in director into a db object
        schema = DirectorSchema()
        update = schema.load(director, session=db.session)

        # Set the id to the director we want to update
        update.id = update_director.id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated director in the response
        data = schema.dump(update_director)

        return data, 200

    # Otherwise, nope, didn't find that director
    else:
        abort(404, f"Director not found for Id: {director_id}")

def delete(director_id):
    """
    This function deletes a person from the people structure
    :param director_id:   Id of the person to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the person requested
    director = Director.query.filter(Director.id == director_id).one_or_none()

    # Did we find a director?
    if director is not None:
        db.session.delete(director)
        db.session.commit()
        return make_response(f"Director with id: {director_id} deleted", 200)

    # Otherwise, nope, didn't find that director
    else:
        abort(404, f"Director not found for Id: {director_id}")
