from flaskr import create_app
from flask_restful import Resource, Api
from .models import Song, SongSchema, db


app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()


song_schema = SongSchema()

class ScoresViews(Resource):
    def get(self):
        return [song_schema.dump(song) for song in Song.query.all()]

    
api = Api(app)
api.add_resource(ScoresViews, '/scores')