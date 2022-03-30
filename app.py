import os

import flask
import requests

app = flask.Flask(__name__)


@app.route('/', methods=['GET'])
def uptime_event():
    return flask.jsonify({
        'uptime': 'Tudo certo por aqui v2',
    })

@app.route('/tasks/<task_id>/score/<direction>', methods=['POST'])
def score_task_event(task_id, direction):
    print('flask.request.environ')
    print(flask.request.environ)

    responses = []

    data = flask.request.json

    for commit in data.get('commits', []):
        valid_users = _get_valid_users()
        if commit['author'].get('email') in valid_users or not valid_users:
            responses.append(score_task(task_id, direction))

    print('responses')
    print(responses)

    print('history_items')
    print(data.get('history_items', {}))

    return flask.jsonify(responses)


def score_task(task_id, direction):
    habitica_url = 'https://habitica.com/api/v3/tasks/{}/score/{}'.format(task_id, direction)

    headers = {
        'x-api-user': os.environ['HABITICA_API_USER'],
        'x-api-key': os.environ['HABITICA_API_KEY']
    }

    response = requests.post(habitica_url, headers=headers)
    return response.json()


def _get_valid_users():
    valid_users = map(str.strip, filter(
        None, os.environ['VALID_USERS'].split(',')))

    print('valid_users')
    print(valid_users)
    
    return valid_users


if __name__ == '__main__':
    app.run()
