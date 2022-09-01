Command to check the logs.


```bash
celery -A flaskr.tasks.tasks worker -l info
```


When you are testing message queue, you can use the following command:


```bash
celery -A tasks.tasks worker -l info -Q log_signin
```

and run flaskr
    
```bash
flask run
```


If you want to test microservices with a message queue, you can use the following command:

For the principal app, into microservices-flask/flaskr/
```bash
flask run
```

For the first microservice, into microservices-flask/microservice1/
```bash
flask run -p 5001
```

For the second microservice, into microservices-flask/microservice2/
```bash
flask run -p 5002
```

FInally, for the message queue into microservices-flask/microservice2/, you can use the following command:
    
```bash
celery -A flaskr.tasks worker -l info
```
For that excercise, you have to set a postgresql database and a redis database.

user: student
password: 1234
dbname: recordsdb

