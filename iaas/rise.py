#!/usr/bin/env python

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return('Hello RISE!')

@app.route('/foo/<string:bar>')
def print_bar(bar):
    return(f'You entered the text:\t{bar}')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
