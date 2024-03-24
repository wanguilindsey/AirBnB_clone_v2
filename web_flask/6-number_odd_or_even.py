#!/usr/bin/python3
"""starts a Flask web application"""


from flask import Flask, render_template
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def cisfun(text):
    return 'C ' + text.replace('_', ' ')


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def pythoniscool(text='is cool'):
    return 'Python ' + text.replace('_', ' ')


@app.route('/number/<int:n>', strict_slashes=False)
def number(num):
    return "{:d} is a number".format(num)


@app.route('/number_template/<int:n>', strict_slashes=False)
def numbertemplate(num):
    return render_template('5-number.html', num=num)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even(num):
    if num % 2 == 0:
        parity = 'even'
    else:
        parity = 'odd'
    return render_template('6-number_odd_or_even.html', num=num, parity=parity)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
