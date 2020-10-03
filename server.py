import json
import time
from datetime import datetime

from apiai import apiai
from flask import Flask, Response, request

app = Flask(__name__)
db = [
    {'text': 'Привет', 'author': 'Jack', 'time': time.time()},
    {'text': 'Приве!', 'author': 'Mary', 'time': time.time()},
]


@app.route("/")
def hello():
    return "Hello, World!<br><a href='/status'>Статус</a><br> <a href='/send_message'>Отправить сообщение</a> <br> <a " \
           "href='/get_messages'>Получить</a> "


def bot(text):

    request = apiai.ApiAI('095918504b2548468d783679235c10e0').text_request() # Токен API к Dialogflow
    request.lang = 'ru' # На каком языке будет послан запрос
    request.session_id = 'BatlabAIBot' # ID Сессии диалога (нужно, чтобы потом учить бота)
    request.query = text # Посылаем запрос к ИИ с сообщением от юзера
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
    # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
    if response:
       return response
    else:
        return 'Нет ответа'

@app.route("/status")
def status():
    dn = datetime.now()
    return {
        'status': True,
        'name': 'Kamaliev, Messenger',
        'time': dn.strftime('%Y-%m-%d %H:%M:%S'),
        'online': len(set([i['author'] for i in db ])),
        'Messages':len([i['text'] for i in db]),
    }


@app.route("/send_message", methods=['POST'])
def send_message():
    data = request.json
    if not isinstance(data, dict):
        return Response('not json', 400)

    text = data.get('text')
    author = data.get('author')

    if isinstance(text, str) and isinstance(author, str):
        db.append({
            'text': text,
            'author': author,
            'time': time.time()
        })
        return Response('ok')
    else:
        return Response('wrong format', 400)


@app.route("/get_messages")
def get_messages():
    after = request.args.get('after', '0')
    try:
        after = float(after)
    except:
        return Response('wrong format', 400)

    new_messages = []
    for m in db:
        if m['time']>after:
            new_messages.append(m)
            if 'Sihnel' == ((str(m['text']).split())[0])[:-1]: # Если есть обращение к боту
                new_messages.append({'text': bot(m['text']), 'author': 'Бот Sihnel', 'time': time.time()})
    return {'messages': new_messages}


app.run()
