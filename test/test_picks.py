import nose
from nose.tools import eq_
from picks import parse
from .data import data_path

TEST_EMAIL_PATH = data_path('email.txt')

def test_parse_body():
    with open(TEST_EMAIL_PATH, 'r') as f:
        parsed = parse(f.read())
        eq_(len(parsed.split('\n')), 14)
