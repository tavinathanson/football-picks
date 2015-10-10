import os
from os import environ
from flask import Flask, request
from flask.json import jsonify
from werkzeug.datastructures import MultiDict
from bs4 import BeautifulSoup
import requests
from six.moves.urllib.parse import unquote_plus
import pandas as pd
from random import choice, sample

app = Flask(__name__)

@app.route('/')
def picks():
    return 'Football picks!'

@app.route('/mail', methods=['POST'])
def mail():
    data = request_dict(request)
    try:
        parsed = parse(data['body-html'])
        parsed = 'Here are my picks:\n%s' % parsed
    except:
        parsed = "I couldn't read this version of the picks email! Oh no!"
    send(parsed)
    return jsonify({'success': True})

def request_dict(request):
    data = request.get_data()
    return MultiDict([part.split("=") for part in data.split("&")])

def parse(body):
    body = unquote_plus(body)
    soup = BeautifulSoup(body, "html.parser")
    tr_tags = soup.find_all('tr')
    pairs = [parse_tr(tr) for tr in tr_tags if len(tr.find_all('td')) == 4 and ' ET' in str(tr)]
    favorites, underdogs = zip(*pairs)
    df_picks = pd.DataFrame({'favorite': favorites, 'underdog': underdogs})
    df_picks['my_pick'] = df_picks.apply(
        lambda row: choice([row['favorite'], row['underdog']]), axis=1)
    best_bets = sample(df_picks.my_pick.unique(), 3)
    df_picks.my_pick = df_picks.my_pick.apply(lambda pick: pick + '***' if pick in best_bets else pick)
    output = '\n'.join(df_picks.my_pick)
    return output

def parse_tr(tr):
    td_tags = tr.find_all('td')
    favorite = str(td_tags[1].get_text())
    underdog = str(td_tags[3].get_text())
    parse_error(is_valid, s=favorite)
    parse_error(is_valid, s=underdog)
    return (favorite, underdog)

def parse_error(true_func, **kwargs):
    if not true_func(**kwargs):
        raise ParseError()

def is_valid(s):
    return not s.isdigit()

def send(text):
    recipient = 'tavi.nathanson@gmail.com'
    request = requests.post(environ['SEND_MAIL_URL'], auth=('api', environ['MAILGUN_API_KEY']), data={
        'from': 'Tavi Nathanson <tavi.nathanson@gmail.com>',
        'to': recipient,
        'subject': 'My football picks!',
        'text': 'Here are my picks! %s' % text
    })

class ParseError(ValueError):
    pass
