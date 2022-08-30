from importlib.metadata import files
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
import enum

db = SQLAlchemy()

album_song = db.Table('album_song',
                      db.Column('album_id', db.Integer, db.ForeignKey(
                          'album.id'), primary_key=True),
                      db.Column('song_id', db.Integer, db.ForeignKey(
                          'song.id'), primary_key=True)
                      )


class Medio(enum.Enum):
    DISC = 1
    CASSETTE = 2
    CD = 3


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    min = db.Column(db.Integer)
    seg = db.Column(db.Integer)
    artist = db.Column(db.String(128))
    albums = db.relationship(
        'Album', secondary='album_song', back_populates='songs')
    __table_args__ = tuple(db.UniqueConstraint('title', name='unique_title'),)

    def __repr__(self):
        return "{}-{}-{}-{}-{}".format(self.id, self.title, self.min, self.seg, self.artist)


class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    year = db.Column(db.Integer)
    description = db.Column(db.String(128))
    media = db.Column(db.Enum(Medio))
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    songs = db.relationship(
        'Song', secondary='album_song', back_populates='albums')
    __table_args__ = tuple(db.UniqueConstraint(
        'user', 'title', name='unique_title'),)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    password = db.Column(db.String(128))
    albums = db.relationship('Album', cascade='all,delete, delete-orphan')


class EnumADictionary(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return {'key': value.name, 'value': value.value}


class AlbumSchema(SQLAlchemyAutoSchema):
    media = EnumADictionary(attribute=('media'))

    class Meta:
        model = Album
        include_relationships = True
        load_instance = True


class SongSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Song
        include_relationships = True
        load_instance = True


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True
