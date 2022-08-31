from celery import Celery

celery_app = Celery(__name__, broker='redis://localhost:6379/0')

@celery_app.task(name="register_log")
def register_log(user, date):
    with open('log_signin.txt', 'a+') as file:
        file.write('{}  - sesion: {}\n'.format(user, date))