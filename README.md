# Vosk Restful Service backed by Flask and Celery

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

Download a vosk model and unzip that in the root of the project as "model" directory.    
https://alphacephei.com/vosk/models

```
wget http://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip
unzip vosk-model-en-us-0.22.zip
mv vosk-model-en-us-0.22 model
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

Response: 
```
{ 
  id: "<task_id>" 
}
```

**Check request status**   
`GET http://localhost:5000/asr/recognize/status/<task_id>`


### Files
`app.py` contains the endpoints functions    
`task.py` contains the script to run Celery and transcribing task function  
`server.py` runs the production API service powered by gevent  

### Notes
This is a very basic example of using Vosk with a task scheduler like Celery. 
You can fork the repo and change the codes and tune Celery configs based on your requirements.
