## Introduction
Welcome to the ticket booking app

## Running the App
```
pip install -r req.txt
python3 app.py
```
In an another terminal(to run the celery beat)

```
 celery -A app.celery worker --loglevel=INFO  -B
```