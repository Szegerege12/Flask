from flask import Flask, abort, request, jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from models import UserModel, RevokedTokenModel
from run import db
import json

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
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message': 'User {} was created'.format(data['username']),
                'acces_token': access_token,
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
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'password': current_user.password,
                'acces_token': access_token,
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


class UserGenerate(Resource):
    """Generate 100 random users"""

    def post(self):
        for i in range(1, 3000):
            new_user = UserModel(
                username=UserModel.random_username(),
                password=UserModel.generate_hash(UserModel.random_password())
            )
            new_user.save_to_db()


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
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong.'}, 500


class TokenRefresh(Resource):
    """Refresh tokena, z wymaganym tokenem od refresha, zaden
    inny nie bedzie tutaj działał"""

    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {
            'username': current_user,
            'new_access_token': access_token
        }


def get_paginated_list(klass, url, start, limit):
    """
    Return paginated list of db Model
    :param klass: dbModel to paginate
    :param url: Api resource url to create next/prev link
    :param start: starting position
    :param limit: limit of position per one page
    :return: paginated list with set parameters
    """
    start = int(start)
    limit = int(limit)
    # check if page exists
    results = klass.return_all()
    # count = (len(results))
    # if count < start:
    # abort(404)

    # make response
    obj = {}
    obj['start'] = start
    obj['limit'] = limit

    # obj['count'] = count
    # make URLs
    # make previous url
    if start == 1:
        obj['previous'] = ''
    else:
        start_copy = max(1, start - limit)
        limit_copy = limit
        obj['previous'] = url + '?start=%d&limit=%d' % (start_copy, limit_copy)

    # make next url
    if start + limit < 1:
        obj['next'] = ''
    else:
        start_copy = start + limit
        obj['next'] = url + '?start=%d&limit=%d' % (start_copy, limit)

    # finally extract result according to bounds
    start_offset = start - 1
    obj['results'] = results['users'][start_offset:start_offset + limit]
    return obj


def get_paginated_list_filter(klass, url, start, limit, query):
    start = int(start)
    limit = int(limit)
    # check if page exists
    results = klass
    # count = (len(results))
    # if count < start:
    # abort(404)

    # make response
    obj = {'sss': 'ss'}
    obj['start'] = start
    obj['limit'] = limit
    #obj['phrase'] = phrase

    # obj['count'] = count
    # make URLs
    # make previous url
    if start == 1:
        obj['previous'] = ''
    else:
        start_copy = max(1, start - limit)
        limit_copy = limit
        obj['previous'] = url + '?query=%s&start=%d&limit=%d' % (query, start_copy, limit)

    # make next url
    if start + limit < 1:
        obj['next'] = ''
    else:
        start_copy = start + limit
        obj['next'] = url + '?query=%s&start=%d&limit=%d' % (query, start_copy, limit)

    # finally extract result according to bounds
    start_offset = start - 1
    obj['results'] = results[(start - 1):(start - 1 + limit)]
    return obj


class AllUsers(Resource):
    def get(self):
        return jsonify(get_paginated_list(
            UserModel,
            'users/page',
            start=request.args.get('start', 1),
            limit=request.args.get('limit', 20)
        ))

    def delete(self):
        return UserModel.delete_all()


class UserFilter(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', help='This field cannot be blank', required=True)
        data = parser.parse_args()
        current_users = UserModel.serialize_list(UserModel.query.filter(
            UserModel.username.like('%' + data['username'] + '%')).all())
        return jsonify(get_paginated_list_filter(
            current_users,
            'filter',
            start=request.args.get('start', 1),
            limit=request.args.get('limit', 20),
            query=data['username']
        ))


class SecretResource(Resource):
    @jwt_required
    def get(self):
        return {
            'answer': 'sekretna odpowiedz'
        }
