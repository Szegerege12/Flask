from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from models import UserModel, RevokedTokenModel
from run import db

# inicjalizacja parsera
parser = reqparse.RequestParser()
parser.add_argument('username', help='This field cannot be blank', required=True)
parser.add_argument('password', help='This field cannot be blank', required=True)


class UserRegistration(Resource):
    """Rejestracja userów, jesli istnieje zwraca komunikat.
    Jeśli nie korzysta z parsera, zbiera dane, hashuje haslo i
    zapisuje do bazy. Dodatkowo tworzy Bearer Token"""

    def post(self):
        data = parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'User {} already exists'.format(data['username'])}

        new_user = UserModel(
            username=data['username'],
            password=UserModel.generate_hash(data['password'])
        )
        try:
            new_user.save_to_db()
            acces_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message': 'User {} was created'.format(data['username']),
                'acces_token': acces_token,
                'refresh_token': refresh_token
            }
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogin(Resource):
    """Logowanie uzytkownika, wymagane username i haslo, jesli jest
    prawidlowe to zwraca dane oraz bearer token który jest uzywany
    przy wymaganych zapytaniach"""

    def post(self):
        data = parser.parse_args()
        current_user = UserModel.find_by_username(data['username'])
        if not current_user:
            return {'message': 'User {} doesnt exist'.format(data['username'])}

        if UserModel.verify_hash(data['password'], current_user.password):
            acces_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'password': current_user.password,
                'acces_token': acces_token,
                'refresh_token': refresh_token
            }
        else:
            return {'message': 'Wrong credentials'}


class PasswordChange(Resource):
    """Zmiana hasla, sprawdza czy podane dane sa prawidlowe, nastepnie
    zmienia haslo na podane w new_password po czym dokonuje update
    bazy danych. Wymagany jest także toekn uzyskiwany podczas logowania"""

    @jwt_required
    def put(self):
        parser.add_argument('new_password', help='New Password')
        data = parser.parse_args()
        current_user = UserModel.find_by_username(data['username'])
        if not current_user:
            return {'message': 'User {} doesnt exist'.format(data['username'])}

        if UserModel.verify_hash(data['password'], current_user.password):
            try:
                current_user.password = UserModel.generate_hash(data['new_password'])
                db.session.commit()
                return {
                    'login': current_user.username,
                    'new password': current_user.password
                }
            except:
                return {'message': 'something went wrong'}


class UserLogoutAcces(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'message': 'Acces token has been revoked'}
        except:
            return {'message': 'Something went wrong.'}, 500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'message': 'Acces token has been revoked'}
        except:
            return {'message': 'Something went wrong.'}, 500


class TokenRefresh(Resource):
    """Refresh tokena, z wymaganym tokenem od refresha, zaden
    inny nie bedzie tutaj działał"""

    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        acces_token = create_access_token(identity=current_user)
        return {'acces_token': acces_token}


class AllUsers(Resource):
    def get(self):
        return UserModel.return_all()

    def delete(self):
        return UserModel.delete_all()


class SecretResource(Resource):
    @jwt_required
    def get(self):
        return {
            'answer': 'sekretna odpowiedz'
        }
