import nose
from nose.tools import eq_, ok_
from picks import parse, request_dict, get_sender, mailer, parse_tr
from .data import data_path
from bs4 import BeautifulSoup

TEST_EMAIL_PATH = data_path('email.txt')
TEST_MAILGUN_PATH = data_path('mailgun.txt')

def test_parse_body():
    with open(TEST_EMAIL_PATH, 'r') as f:
        body, week = parse(f.read())
        eq_(len(body.split('\n')), 14)
        eq_(week, '5')

def test_parse_no_picks():
    with open(TEST_MAILGUN_PATH, 'r') as f:
        to, subject, body = mailer(request_dict(f.read()))
        ok_('Oh no!' in body)

def test_sender():
    with open(TEST_MAILGUN_PATH, 'r') as f:
        data = request_dict(f.read())
        to = get_sender(data)
        eq_(to, 'adam.smith@example.com')

def test_parens():
    tr_region = BeautifulSoup(('<td>Date</td><td>Seattle</td>'
                               '<td>Spread</td><td>Hello (Goodbye)</td>'),
                              'html.parser')
    favorite, underdog = parse_tr(tr_region)
    eq_(favorite, 'Seattle')
    eq_(underdog, 'Hello')
