from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm

#  strona głowna
@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Marek'}  # mock user ( żeby nie zaprzątać sobie głowy brakiem userów)
    posts = [
        {
            'author':{'username': 'Marek'},
            'body': 'Piękny dziś dzien w Warszawie'
        },
        {
            'author': {'username': 'Kamil'},
            'body': 'Lubię film Gladiator.'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)


#  logowanie
@app.route('/login', methods=['GET', 'POST'])  #  dodanie metod get i post - pokazywanie i odbiranie danych do serwera
def login():
    form = LoginForm()
    if form.validate_on_submit():  # jesli pola sa wypelnione sprawdza walidatory
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))  #  po nacisnieciu sign in powraca do indexa
    return render_template('login.html', title='Sign In', form=form)  #  renderowanie


