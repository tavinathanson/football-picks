import os
from flask import Flask
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def picks():
    return 'Football picks!'

def parse(file_name):
    with open(file_name, 'r') as f:
        soup = BeautifulSoup(f, "html.parser")
        tr_tags = soup.find_all('tr')
        return len(tr_tags)
