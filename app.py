import os

import flask
import requests

app = flask.Flask(__name__)


@app.route('/', methods=['GET'])
def uptime_event():
    return flask.jsonify({
        'uptime': 'Tudo certo por aqui 2.2',
    })

@app.route('/tasks/<task_id>/score/<direction>', methods=['POST'])
def score_task_event(task_id, direction):
    print('-- flask.request.environ 2.2 --')
    print(flask.request.environ)

    responses = []

    data = flask.request.json

    print('-- data --')
    print(data)

    # for github integration
    for commit in data.get('commits', []):
        valid_users = _get_valid_users()

        print('-- commit author --')
        print(commit['author'].get('email'))
        print('-- valid user --')
        print(commit['author'].get('email') in valid_users)

        if commit['author'].get('email') in valid_users or not valid_users:
            print('-- call score_task --')
            print(task_id)
            print(direction)
            responses.append(score_task(task_id, direction))

    # for habitica integration
    for historyItem in data.get('history_items', []):
        valid_users = _get_valid_users()

        print('-- historyItem user --')
        print(historyItem['user'].get('email'))
        print('-- valid user --')
        print(historyItem['user'].get('email') in valid_users)
        print('-- after type closed --')
        print(historyItem['after'].get('type') == 'closed')

        isValidUser = historyItem['user'].get('email') in valid_users or not valid_users
        isStatusClosed = historyItem['after'].get('type') == 'closed'
        if isValidUser and isStatusClosed:
            print('-- call score_task --')
            print(task_id)
            print(direction)
            responses.append(score_task(task_id, direction))

    print('-- responses --')
    print(responses)

    return flask.jsonify(responses)


def score_task(task_id, direction):
    habitica_url = 'https://habitica.com/api/v3/tasks/{}/score/{}'.format(task_id, direction)

    print('-- habitica_url --')
    print(habitica_url)

    headers = {
        'x-api-user': os.environ['HABITICA_API_USER'],
        'x-api-key': os.environ['HABITICA_API_KEY']
    }

    response = requests.post(habitica_url, headers=headers)
    return response.json()


def _get_valid_users():
    valid_users = map(str.strip, filter(
        None, os.environ['VALID_USERS'].split(',')))

    return valid_users


if __name__ == '__main__':
    app.run()
