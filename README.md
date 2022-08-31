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
