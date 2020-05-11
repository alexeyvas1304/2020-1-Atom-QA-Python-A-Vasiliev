import threading
from flask import Flask, abort, request
from user_data import SOCKET_HOST, SOCKET_PORT

app = Flask(__name__)

host = SOCKET_HOST
port = SOCKET_PORT

users = {}


def run_mock():
    server = threading.Thread(target=app.run, kwargs={'host': host, 'port': port})
    server.start()
    return server


def shutdown_mock():
    terminate_func = request.environ.get('werkzeug.server.shutdown')
    if terminate_func:
        terminate_func()


@app.route('/shutdown')
def shutdown():
    shutdown_mock()


@app.route('/users/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = users.get(int(user_id), None)
    if user:
        return user
    else:
        abort(404)


@app.route('/users', methods=['POST'])
def post_user():
    new_user = {"name": request.form.get("name"), "surname": request.form.get("surname")}
    users.update({len(users): new_user})  # исходя из предположения, что ничего не удаляется
    return "OK"


if __name__ == '__main__':
    # WSGIRequestHandler.protocol_version = "HTTP/1.1" # была попытка keepalive
    run_mock()
