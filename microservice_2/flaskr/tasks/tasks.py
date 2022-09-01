from ..app import db
from ..models import Song, SongSchema
import os
from celery import Celery
from celery.signals import task_postrun


celery_app = Celery('tasks', broker='redis://localhost:6379/0')


song_schema = SongSchema()

@celery_app.task(name='tasks.scores')
def register_score(song_json):
    song = Song.query.get(song_json["id"])
    if song is None:
        song = Song( title=song_json['title'], min=song_json['min'], seg=song_json['seg'], artist=song_json['artist'], scores=[song_json['score']])
        db.session.add(song)
        db.session.commit()
    else:
        song.scores = song.scores + [song_json['score']]
    db.session.commit()

@task_postrun.connect()
def close_db_session(*args, **kwargs):
    db.session.remove()
    
    