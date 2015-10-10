import os
from os import environ
from flask import Flask, request
from flask.json import jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route('/')
def picks():
    return 'Football picks!'

@app.route('/mail', methods=['POST'])
def mail():
    data = request.get_data()
    send()
    return jsonify({'url': environ['SEND_MAIL_URL']})

def parse(file_name):
    with open(file_name, 'r') as f:
        soup = BeautifulSoup(f, "html.parser")
        tr_tags = soup.find_all('tr')
        return len(tr_tags)

def send():
    recipient = 'tavi.nathanson@gmail.com'
    request = requests.post(environ['SEND_MAIL_URL'], auth=('api', environ['MAILGUN_API_KEY']), data={
        'from': 'Tavi Nathanson <tavi.nathanson@gmail.com>',
        'to': recipient,
        'subject': 'My football picks!',
        'text': 'Here are my picks!'
    })
