from tools.api import find_member_info
from panel.data.models.all_users import User
from panel.data.models.conference_user import ConferenceUser
from panel.data.models.staistics import Statistics


def new_user(member):
    user = User()

    user.user_id = member['id']
    user.name = member['first_name']
    user.surname = member['last_name']
    user.sex = member['sex']
    user.is_closed = member['is_closed']

    return user


def new_conf_user(member, peer_id, members_info):
    conference_user = ConferenceUser()

    conference_user.user_id = member['id']
    conference_user.conference_id = peer_id
    conference_user.invited_by, \
    conference_user.is_admin, \
    conference_user.is_owner, \
    conference_user.join_date = find_member_info(member['id'], members_info['items'])

    if conference_user.is_admin:
        conference_user.kick = True
        conference_user.warn = True

    return conference_user
