from gevent.pywsgi import WSGIServer
from app import api

http_server = WSGIServer(('', 5000), api)
http_server.serve_forever()
