#!/usr/bin/python3
"""starts a Flask web application"""


from flask import Flask, render_template
from models import *
from models import storage
app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    return render_template(
            '8-cities_by_state.html', states=storage.all("State"))


@app.teardown_appcontext
def teardown(err):
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
