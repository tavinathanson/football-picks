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
    data = request_dict(request.get_data())
    to, subject, body = mailer(data)
    send(to=to, subject=subject, body=body)
    return jsonify({'success': True})

def mailer(data):
    try:
        body, week = parse(data['body-html'])
        body = 'Here are my picks for week %s:\n\n%s' % (week, body)
        subject="My picks for week %s!" % week
    except:
        body = 'I couldn\'t read this version of the picks email! Oh no!'
        subject = 'No picks for you!'
    return get_sender(data), subject, body

def get_sender(data):
    return unquote_plus(data['sender'])

def request_dict(data):
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
    best_bets = sample(set(df_picks.my_pick.unique()), 3)
    df_picks.my_pick = df_picks.my_pick.apply(lambda pick: pick + '***' if pick in best_bets else pick)
    df_picks.my_pick = df_picks.my_pick.apply(lambda pick: pick[3:] if pick.startswith('At ') else pick)
    body_output = '\n'.join(df_picks.my_pick)
    text_joined = ''.join(soup.get_text()).lower()
    text_joined = text_joined.replace('last week', '').replace('other week', '').replace('this week', '')
    text_parts = text_joined.split(" ")
    week_index = text_parts.index("week")
    week_num = text_parts[week_index + 1]
    return body_output, week_num

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

def send(to, subject, body):
    admin = '%s <%s>' % (environ['ADMIN_NAME'], environ['ADMIN_EMAIL'])
    request = requests.post(environ['SEND_MAIL_URL'], auth=('api', environ['MAILGUN_API_KEY']), data={
        'from': admin,
        'to': to,
        'bcc': admin,
        'subject': subject,
        'text': body
    })

class ParseError(ValueError):
    pass
