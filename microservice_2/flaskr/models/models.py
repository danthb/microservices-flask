from importlib.metadata import files
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

db = SQLAlchemy()

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    min = db.Column(db.Integer)
    seg = db.Column(db.Integer)
    artist = db.Column(db.String(128))
    scores = db.Column( db.ARRAY(db.Float))


class SongSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Song
        load_instance = True