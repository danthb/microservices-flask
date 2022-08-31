from os import access
import queue
from flask_restful import Resource
from ..models import db, Song, SongSchema, User, UserSchema, Album, AlbumSchema, Medio
from flask import request
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from datetime import datetime
from celery import Celery

celery_app = Celery(__name__, broker='redis://localhost:6379/0')

@celery_app.task(name="register_log")
def register_log(*args, **kwargs):
    pass


song_schema = SongSchema()
user_schema = UserSchema()
album_schema = AlbumSchema()


class SongsView(Resource):
    def get(self):
        return [song_schema.dump(song) for song in Song.query.all()]
    
    def post(self):
        new_song = Song(
                                title=request.json['title'], 
                                min=request.json['min'], 
                                seg=request.json['seg'], 
                                artist=request.json['artist'])
    
        db.session.add(new_song)
        db.session.commit()
        return song_schema.dump(new_song)
    
    
class SongView(Resource):
    def get(self, id):
        return song_schema.dump(Song.query.get_or_404(id))
    
    def put(self, id):
        song = Song.query.get_or_404(id)
        song.title = request.json.get('title', song.title)
        song.min = request.json.get('min', song.min)
        song.seg = request.json.get('seg', song.seg)
        song.artist = request.json.get('artist', song.artist)
        db.session.commit()
        return song_schema.dump(song) 
    
    
    def delete(self, id):
        song = Song.query.get_or_404(id)
        db.session.delete(song)
        db.session.commit()
        return 'Ok', 204
    
    
class LogInView(Resource):
    def post(self):
        u_name = request.json["name"]
        u_password = request.json["password"]
        user = User.query.filter_by(name=u_name, password = u_password).all()
        if user:
            args = (u_name, datetime.now())
            register_log.apply_async(args=args, queue='log_signin')
            return {'message':'LogIn successful'}, 200
        else:
            return {'message':'Wrong credentials'}, 401
            
class LogOutView(Resource):
    
    def post(self):
        return {'message':'LogOut successful'}, 200
    
    
class SignInView(Resource):
    
    def post(self):
        new_user = User(name=request.json["name"], password=request.json["password"])
        access_token = create_access_token(identity=new_user.name)
        db.session.add(new_user)
        db.session.commit()
        return {'message':'SignIn successful', 'access_token':access_token}, 200 

    def put(self, id_user):
        user = User.query.get_or_404(id_user)
        user.password = request.json.get("password",user.password)
        db.session.commit()
        return user_schema.dump(user)

    def delete(self, id_user):
        user = User.query.get_or_404(id_user)
        db.session.delete(user)
        db.session.commit()
        return '',204

class AlbumsUserView(Resource):
    
    @jwt_required()
    def post(self, id_user):
        nuevo_album = Album(title=request.json["title"], year=request.json["year"], description=request.json["description"], medio=request.json["medio"])
        user = User.query.get_or_404(id_user)
        user.albumes.append(nuevo_album)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return 'user has a album with name',409

        return album_schema.dump(nuevo_album)
    
    
    @jwt_required()
    def get(self, id_user):
        user = User.query.get_or_404(id_user)
        return [album_schema.dump(al) for al in user.albums]

class SongsAlbumVIew(Resource):

    def post(self, id_album):
        album = Album.query.get_or_404(id_album)
        
        if "id_song" in request.json.keys():
            
            nueva_songs = Song.query.get(request.json["id_song"])
            if nueva_songs is not None:
                album.songses.append(nueva_songs)
                db.session.commit()
            else:
                return 'Canción errónea',404
        else: 
            nueva_songs = Song(title=request.json["title"], minutos=request.json["minutos"], segundos=request.json["segundos"], interprete=request.json["interprete"])
            album.songses.append(nueva_songs)
        db.session.commit()
        return song_schema.dump(nueva_songs)
       
    def get(self, id_album):
        album = Album.query.get_or_404(id_album)
        return [song_schema.dump(ca) for ca in album.songs]

class AlbumView(Resource):

    def get(self, id_album):
        return album_schema.dump(Album.query.get_or_404(id_album))

    def put(self, id_album):
        album = Album.query.get_or_404(id_album)
        album.title = request.json.get("title",album.title)
        album.year = request.json.get("year", album.year)
        album.description = request.json.get("description", album.description)
        album.medio = request.json.get("medio", album.medio)
        db.session.commit()
        return album_schema.dump(album)

    def delete(self, id_album):
        album = Album.query.get_or_404(id_album)
        db.session.delete(album)
        db.session.commit()
        return '',204

