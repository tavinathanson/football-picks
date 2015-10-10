import nose
from nose.tools import eq_
from picks import parse
from .data import data_path

TEST_EMAIL_PATH = data_path('email.txt')

def test_parse_body():
    with open(TEST_EMAIL_PATH, 'r') as f:
        body, week = parse(f.read())
        eq_(len(body.split('\n')), 14)
        eq_(week, '5')
