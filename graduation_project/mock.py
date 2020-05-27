import threading

from flask import Flask, request, jsonify

app = Flask(__name__)

host = 'mock_vk'  # интересно
port = 5000
users = {'alexey': '1', 'sergey': '2', 'ilya': '3', 'kirill': '4', 'qwerty': '5', 'superuser': '6',
         'ultrahero': '7' * 300}


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


@app.route('/vk_id/<username>')
def get_id_by_username(username):
    if username in users:
        return {'vk_id': users[username]}
    else:
        response = jsonify({})
        response.status_code = 404
        return response


@app.route('/vk_id/add_user', methods=['POST'])
def post_user():
    name = request.form.get("name")
    id = request.form.get("id")
    users.update({name: id})
    return "OK"


if __name__ == '__main__':
    run_mock()
