from run import app, db
from flask import jsonify, render_template


@app.route('/login', methods=['GET'])
def index():
    users = db.filter_by
    return render_template('home.html', users=users)
