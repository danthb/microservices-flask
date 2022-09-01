import json
from microservice_1 import create_app
from flask_restful import Resource, Api
from flask import Flask, request
import requests
import json
from celery import Celery

celery_app = Celery(__name__, broker='redis://localhost:6379/0')

app = create_app('default')
app_context = app.app_context()
app_context.push()

api = Api(app)

@celery_app.task(name='tasks.scores')
def register_score(song_json):
    pass

class ScoreView(Resource):
    def post(self, id_song):
        content = requests.get('http://127.0.0.1:5000/song/{}'.format(id_song))
        
        if content.status_code == 404:
            return content.json(), 404
        else:
            song = content.json()
            song['score'] = request.json['score'] 
            args = (song,)
            register_score.apply_async(args)
            return json.dumps(song)


api.add_resource(ScoreView, '/song/<int:id_song>/score')