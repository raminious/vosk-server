from flask import Flask, jsonify
from jobs import recognize
import json

api = Flask(__name__)


@api.route('/asr/recognize', methods=['POST'])
def transcribe():
  # an example for passing data to the job
  data = {
      'filepath': './files/test.wav'
  }

  task = recognize.apply_async(args=[data])

  return {
      'id': task.id
  }


@api.route('/asr/recognize/status/<task_id>', methods=['GET'])
def result(task_id):
  task = recognize.AsyncResult(task_id)
  if task.state == 'PENDING':
    response = {
        'state': task.state,
    }
  elif task.state == 'SUCCESS':
    response = {
        'state': task.state,
        'data': json.loads(task.info)
    }

  else:
    response = {
        'state': task.state,
        'status': str(task.info)
    }

  return jsonify(response)


if __name__ == '__main__':
  api.run()
