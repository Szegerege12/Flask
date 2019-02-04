from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash   # moduly do tworzenia hasel i sprawdzannia po hashu
from flask_login import UserMixin
from hashlib import md5


# tabela pomocnicza przechowująca jedynie klucze obce, więc nie ma sensu robienia jej na modelu klasy
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


# klasa użytkownika
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

# metody klasy User
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        """Funkcja tworzy haslo hash"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Funkcja sprawdzajaca zgodnosc hasla"""
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        """Funkcja generująca avatar na podstawie emaila za pomocą
        strony gravatar."""
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def follow(self,user):
        """Metoda słuząca do followania usera wraz z metoda wspomagajaca"""
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self,user):
        """Metoda do przestanai sledzenia uzytkownika z metoda wspomagajaca"""
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self,user):
        """Sprawdza czy istnieje relacja follow miedzy userami"""
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        """Łaczy ze sobą sledzonych uzytkowników wraz z ich postami.
        Baza danych ma tworzyć tymczasową tabele, która łączy dane
        z tabel i postów obserwatorów. Za pomocą operatora "union'
        łaczę dwa zapytania w jedno( posty followed osób i moje własne
        """
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
            followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

#  loader uzyytkowniów
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)



