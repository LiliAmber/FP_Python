from config import db, ma
from marshmallow import fields
from sqlalchemy.orm import relationship
from flask import abort
from sqlalchemy.orm import validates
import re

class Director(db.Model): 
    __tablename__ = 'directors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    gender = db.Column(db.Integer)
    uid = db.Column(db.Integer)
    department = db.Column(db.Text)

    movies = relationship("Movie")

    # validasi
    @validates('gender')
    def validate_gender(self, key, value):
        valid_gender = [0, 1, 2]
        if value not in valid_gender:
            abort(
                status=400,
                description=f"Please insert gender with value: 0  -> i prefer not to say , 1 -> for female, 2 -> for male "
            )
        if not value:
            abort(
                status=400,
                description="gender can't be empty"
            )
        return value
    
    @validates('uid')
    def validate_uid(self, key, uid):
        if not uid:
            abort(
                status=400,
                description="uid can't be empty"
            )
        # if Director.query.filter(Director.uid == uid).first():
        #     abort(
        #         status=400,
        #         description=f"director with uid {uid} already exists, please insert another value"
        #     )
        return uid

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            abort(
                status=400,
                description="name can't be empty"
            )
        if len(name) < 5 or len(name) > 20:
            abort(
                status=400,
                description='name must be between 5 and 20 characters'
            )
        # if Director.query.filter(Director.name == name).first():
        #     abort(
        #         status=400,
        #         description=f"director with name {name} already exists, please insert another value"
        #     )
        return name
    
    @validates('departement')
    def validate_department(self, key, department):
        if not department:
            abort(
                status=400,
                description="department can't be empty"
            )
        
        return department

class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    original_title = db.Column(db.Text, nullable=False)
    budget = db.Column(db.Integer)
    popularity = db.Column(db.Integer)
    revenue = db.Column(db.Integer)
    title = db.Column(db.Text)
    vote_average = db.Column(db.REAL)
    vote_count = db.Column(db.Integer)
    overview = db.Column(db.Text)
    tagline = db.Column(db.Text)
    uid = db.Column(db.Integer)
    release_date = db.Column(db.String)
    
    director_id = db.Column(db.Integer, db.ForeignKey('directors.id'))
    director = relationship("Director", back_populates="movies")

    # validasi
    @validates('uid')
    def validate_uid(self, key, uid):
        if not uid:
            abort(
                status=400,
                description="uid can't be empty"
            )
        # if Director.query.filter(Movie.uid == uid).first():
        #     abort(
        #         status=400,
        #         description=f"movie with uid {uid} already exists, please insert another value"
        #     )
        return uid
    
    @validates('release_date')
    def validate_release_date(self, key, date):
        if not date:
            abort(
                status=400,
                description="release date can't be empty"
            )
        if not re.match("^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$", date):
            abort(
                status=404,
                description="please insert release date with valid format (yyyy-mm-dd)"
            )
        return date
    
    @validates('original_title')
    def validate_original_title(self, key, value):
        if not value:
            abort(
                status=400,
                description="original title is required"
            )
        return value

    @validates('title')
    def validate_original_title(self, key, value):
        if not value:
            abort(
                status=400,
                description="title is required"
            )
        return value
    
    @validates('budget')
    def validate_budget(self, key, budget):
        if not budget:
            abort(
                status=400,
                description="budget can't be empty"
            )
        return budget
    
    @validates('popularity')
    def validate_popularity(self, key, popularity):
        if not popularity:
            abort(
                status=400,
                description="popularity is required"
            )
        return popularity
    
    @validates('revenue')
    def validate_revenue(self, key, revenue):
        if not revenue:
            abort(
                status=400,
                description="revenue is required"
            )
        return revenue

    @validates('vote_average')
    def validate_vote_average(self, key, vote_average):
        if not vote_average:
            abort(
                status=400,
                description="vote average is required"
            )
        return vote_average

    @validates('vote_account')
    def validate_vote_count(self, key, vote_count):
        if not vote_count:
            abort(
                status=400,
                description="vote count is required"
            )
        return vote_count

    @validates('overview')
    def validate_overview(self, key, overview):
        if not overview:
            abort(
                status=400,
                description="overview is required"
            )
        return overview

    @validates('tagline')
    def validate_tagline(self, key, tagline):
        if not tagline:
            abort(
                status=400,
                description="tagline is required"
            )
        return tagline

class DirectorSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Director
        sqla_session = db.session
        load_instance = True

    movies = fields.Nested('DirectorMovieSchema', default=[], many=True)

class DirectorMovieSchema(ma.SQLAlchemyAutoSchema):
    """
    This class exists to get around a recursion issue
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    id = fields.Int()
    director_id = fields.Int()
    original_title = fields.Str()
    budget = fields.Int()
    popularity = fields.Int()
    release_date = fields.Str()
    revenue = fields.Int()
    title = fields.Str()
    vote_average = fields.Float()
    vote_count = fields.Int()
    overview = fields.Str()
    tagline = fields.Str()
    uid = fields.Int()

class MovieSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Movie
        sqla_session = db.session
        load_instance = True
        
    director = fields.Nested("MovieDirectorSchema", default=None)

class MovieDirectorSchema(ma.SQLAlchemyAutoSchema):
    """
    This class exists to get around a recursion issue
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    #
    id = fields.Int()
    name = fields.Str()
    gender = fields.Int()
    uid = fields.Int()
    department = fields.Str()