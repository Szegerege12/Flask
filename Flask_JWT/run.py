from flask import Flask
from flask_restful import Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# instancja
app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)
CORS(app)

# configi
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'tu-powinno-byc-cos-secret'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

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

api.add_resource(resources.UserRegistration, '/registration') #done
api.add_resource(resources.UserLogin, '/login') #done
api.add_resource(resources.UserLogoutAcces, '/logout/acces')
api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(resources.TokenRefresh, '/token/refresh') # done
api.add_resource(resources.AllUsers, '/users') #done
api.add_resource(resources.SecretResource, '/secret')
api.add_resource(resources.PasswordChange, '/update') #done

