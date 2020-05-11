from flask import jsonify
from flask_restful import abort, Resource, reqparse

from panel.data import db_session
from panel.data.models.all_users import User
from panel.data.models.api_key import ApiKey
from panel.data.models.conference_user import ConferenceUser

parser = reqparse.RequestParser()
parser.add_argument('job', required=True)
parser.add_argument('work_size', required=True, type=int)
parser.add_argument('collaborators', required=True)
parser.add_argument('is_finished', required=True, type=bool)
parser.add_argument('team_leader', required=True, type=int)


def check_api_key(key):
    session = db_session.create_session()
    api_key = session.query(ApiKey).filter(ApiKey.key == key)
    if api_key:
        return [cu.conference_id for cu in
                session.query(ConferenceUser).filter(ConferenceUser.user_id == api_key.user_id).all()]
    return None


class UsersResource(Resource):
    def get(self, key, job_id):
        session = db_session.create_session()
        user = session.query(User).get(job_id)
        return jsonify({'job': user.to_dict()})
        2


class UsersListResource(Resource):
    def get(self, key):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'news': [user.to_dict()
                                 for user in users]})


if __name__ == '__main__':
    pass
