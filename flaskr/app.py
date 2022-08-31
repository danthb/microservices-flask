from flaskr import create_app
from flask_restful import Api
from flask_jwt_extended import JWTManager

from flaskr.views.views import LogOutView
from .models import db
from .views import SongsView, SongView, LogInView,  LogOutView  ,SignInView,  AlbumView, AlbumsUserView, SongsAlbumVIew

app = create_app('default')
app_context = app.app_context()
app_context.push()


db.init_app(app)
db.create_all()


api = Api(app)
api.add_resource(SongsView, '/songs')
api.add_resource(SongView, '/song/<int:id>')
api.add_resource(SignInView, '/signin')
api.add_resource(LogInView, '/login')
api.add_resource(LogOutView, '/logout')
api.add_resource(AlbumsUserView, '/user/<int:id_user>/albums')
api.add_resource(AlbumView, '/album/<int:id_album>')
api.add_resource(SongsAlbumVIew, '/album/<int:id_album>/songs')

jwt = JWTManager(app)   


#TESTING
""" with app.app_context():
    album_schema = AlbumSchema()
    s = Song(title='Taking to the moon', min=2, seg=40, artist='Bruno Mars')
    s1 = Song(title='Harry Styles', min=2, seg=40, artist='Bruno Parts')
    u = User(name='Daniel', password='1234' )
    u1 = User(name='Lourdes', password='1234' )
    a = Album(title='Back to home', year=1980, description='text', media=Medio.CD)
    a1 = Album(title='Live', year=1981, description='text in the world', media=Medio.CD)
    db.session.add(a)
    db.session.add(s1)
    a.songs.append(s1)
    db.session.commit()
    print([album_schema.dumps(album) for album in Album.query.all()]) """
