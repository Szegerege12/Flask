from flask import Flask
from flask_restful import Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# instancja
app = Flask(__name__)
api = Api(app)

# configi
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'tu-powinno-byc-cos-secret'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['acces', 'refresh']

jwt = JWTManager(app)

# baza danych
db = SQLAlchemy(app)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    """Sprawdza czy token jest na czarnej liscie"""
    jti = decrypted_token['jti']
    return models.RevokedTokenModel.is_jti_blacklisted(jti)


@app.before_first_request
def create_tables():
    """Tworzenie bazy danych przed pierwszym requestem"""
    db.create_all()


import views, models, resources

# rejestracja endpointów

api.add_resource(resources.UserRegistration, '/registration')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.UserLogoutAcces, '/logout/acces')
api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(resources.TokenRefresh, '/token/refresh')
api.add_resource(resources.AllUsers, '/users')
api.add_resource(resources.SecretResource, '/secret')
