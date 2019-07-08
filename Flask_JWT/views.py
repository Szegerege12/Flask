from run import app, db
from flask import jsonify, render_template


@app.route('/')
def index():
    return render_template('home.html')


