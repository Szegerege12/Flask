import requests
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), )


@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        new_city = request.form.get('city')

        if new_city:
            new_city_obj = City(name=new_city)
            db.session.add(new_city_obj)
            db.session.commit()

    cities = City.query.all()

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=9d3f3ae1e6f0b449f3d8d3673f807365'

    weather_data = []
    for city in cities:
        r = requests.get(url.format(city.name)).json()

        weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon']
        }

        weather_data.append(weather)

    return render_template('index.html', weather_data=weather_data)


@app.route('/clear', methods=['GET','POST'])
def clear():
    db.session.query(City).delete()
    db.session.commit()
    return render_template('clear.html')

