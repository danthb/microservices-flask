import json
from microservice_1 import create_app
from flask_restful import Resource, Api
from flask import Flask, request
import requests
import json

app = create_app('default')
app_context = app.app_context()
app_context.push()


api = Api(app)


class ScoreView(Resource):
    def post(self, id_song):
        content = requests.get('http://127.0.0.1:5000/song/{}'.format(id_song))
        
        if content.status_code == 404:
            return content.json(), 404
        else:
            song = content.json()
            song['score'] = request.json['score'] 
            args = (song,)
            return json.dumps(song)


api.add_resource(ScoreView, '/song/<int:id_song>/score')