import nose
from nose.tools import eq_
from picks import parse
from .data import data_path

TEST_FILE_PATH = data_path('test.html')

def test_parse():
    eq_(parse(TEST_FILE_PATH), 16)

