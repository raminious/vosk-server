from flask import Flask, jsonify, request
from tasks import recognize
from os import remove
import json
import tempfile

api = Flask(__name__)


@api.route('/asr/recognize', methods=['POST'])
def transcribe():
    if request.content_type != 'audio/x-wav':
        return jsonify({
            'msg': "415 Unsupported Media Type ;)"
        }), 415

    data = None
    if request.headers.get('Transfer-Encoding') == 'chunked':
        data = request.stream
    elif request.data:
        data = request.data

    if data is None:
        return jsonify({
            'msg': "400 No data found ;)"
        }), 400

    fp = tempfile.NamedTemporaryFile(delete=False)
    fp.write(data)

    task = recognize.apply_async(args=[{
        'filename': fp.name
    }])

    return jsonify({
        'id': task.id
    })


@api.route('/asr/recognize/status/<task_id>', methods=['GET'])
def result(task_id):
    task = recognize.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
        }
    elif task.state == 'SUCCESS':
        try:
            remove(task.args[0]['filename'])
        except FileNotFoundError:
            pass
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
