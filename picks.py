import os
from os import environ
from flask import Flask, request
from flask.json import jsonify
from werkzeug.datastructures import MultiDict
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route('/')
def picks():
    return 'Football picks!'

@app.route('/mail', methods=['POST'])
def mail():
    data = request_dict(request)
    send(str(data['body-plain']))
    return jsonify({'url': environ['SEND_MAIL_URL']})

def request_dict(request):
    data = request.get_data()
    return MultiDict([part.split("=") for part in data.split("&")])

def parse(file_name):
    with open(file_name, 'r') as f:
        soup = BeautifulSoup(f, "html.parser")
        tr_tags = soup.find_all('tr')
        return len(tr_tags)

def send(text):
    recipient = 'tavi.nathanson@gmail.com'
    request = requests.post(environ['SEND_MAIL_URL'], auth=('api', environ['MAILGUN_API_KEY']), data={
        'from': 'Tavi Nathanson <tavi.nathanson@gmail.com>',
        'to': recipient,
        'subject': 'My football picks!',
        'text': 'Here are my picks! %s' % text
    })
