from config import db, ma
from marshmallow import fields
from sqlalchemy.orm import relationship

class Director(db.Model): 
    __tablename__ = 'directors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    gender = db.Column(db.Integer)
    uid = db.Column(db.Integer)
    department = db.Column(db.Text)

    # movie = db.relationship(
    #     'Movie',
    #     backref='directors',
    #     cascade='all, delete, delete-orphan',
    #     single_parent=True,
    #     order_by='asc(Movie.id)'
    # )
    movies = relationship("Movie")

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
    # timestamp = db.Column(
    #     db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    # )

    director_id = db.Column(db.Integer, db.ForeignKey('directors.id'))
    # director = db.relationship(
    #     'Director',
    #     backref='movies',
    #     cascade='all, delete, delete-orphan',
    #     single_parent=True,
    #     order_by='asc(Director.id)'
    # )
    # director = relationship("Director")
    director = relationship("Director", back_populates="movies")

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