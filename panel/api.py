from flask import jsonify
from flask_restful import abort, Resource, reqparse

from panel.data import db_session
from panel.data.models.all_users import User
from panel.data.models.api_key import ApiKey
from panel.data.models.conference_user import ConferenceUser


def check_api_key(key):
    session = db_session.create_session()
    api_key = session.query(ApiKey).filter(ApiKey.key == key).first()
    if api_key:
        return [cu.conference_id for cu in
                session.query(ConferenceUser).filter(ConferenceUser.user_id == api_key.user_id).all()]
    return None


class UsersResource(Resource):
    def get(self, key, user_id):
        if check_api_key(key):
            session = db_session.create_session()
            user = session.query(User).filter(User.user_id == user_id).first()
            print(user)
            return jsonify({'user': user.to_dict(only=('name', 'surname', 'sex', 'msg_count'))})
        return jsonify({'error': 'invalid api key'})


class UsersListResource(Resource):
    def get(self, key, conference_id):
        if check_api_key(key) and conference_id in check_api_key(key):
            session = db_session.create_session()
            users = session.query(ConferenceUser).filter(ConferenceUser.conference_id == conference_id).all()
            print(users)
            return jsonify(
                {'users': [user.to_dict(only=('user_id', 'conference_id', 'msg_count', 'is_admin', 'is_leave'))
                           for user in users]})
