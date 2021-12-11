# Vosk Restful Service backed by Flask and Celery (Redis)

### How to Setup

Clone it first
```
git clone git@github.com:raminious/vosk-server.git
cd vosk-server
```

Create Virtual Env (optional)
```
python -m venv env
source env/bin/activate
```

Install requirements
```
pip install -r requirements.txt
```

Run in Development environment
```
python app.py
python tasks.py # in another terminal
```

Run in Production environment
```
python server.py
python tasks.py 
```

### Endpoints

**Send a new transcribe request**
`POST http://localhost:5000/asr/recognize` 
returns `{ id: "<task_id>" }` as JSON

**Check request status**
`GET http://localhost:5000/asr/recognize/status/<task_id>`

### Note

This is a very basic example of using Vosk with a task scheduler like Celery. 

`app.py` contains the endpoints functions    
`task.py` contains the script to run Celery and transcribing task function  
`server.py` runs the production API service powered by gevent  

You can fork the repo and change the codes and tune Celery configs based on your requirements.