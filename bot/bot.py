from tools.api import VkApi, find_member_info
from tools.loaders import message_loader, photo_loader
from tools.other import event_pprint
from vk_api.bot_longpoll import VkBotEventType

from panel.data import db_session
from panel.data.db_session import create_session
from panel.data.models.all_conferences import Conference
from panel.data.models.all_users import User
from panel.data.models.conference_user import ConferenceUser
from panel.data.models.conferences_queue import ConferencesQueue


class GodBotVk:
    def __init__(self):
        self.VkApi = VkApi()
        try:
            self.session = create_session()
        except TypeError:
            db_session.global_init()
            self.session = create_session()

    def start_pooling(self):
        create_session()
        for event in self.VkApi.LongPool.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:

                # print('=====================')
                # event_pprint(event)
                # print('=====================')

                message_object = event.obj.message
                if message_object['peer_id'] > 2000000000:  # Беседки
                    self.conference(event)
                else:  # Люди и нелюди
                    pass

    def conference(self, event):
        message_object = event.obj.message
        peer_id = message_object['peer_id']
        if message_object.get('action', 0):  # Тут ивент приглашения
            self.chat_action(message_object)
        else:
            queued = self.session.query(ConferencesQueue).filter(ConferencesQueue.conference_id == peer_id).first()
            if queued:  # Ждем админа
                if self.VkApi.check_admin_permission(peer_id):
                    self.session.delete(queued)
                    self.session.commit()
                    self.VkApi.message_send(peer_id,
                                            message_loader('get_admin_rights.txt'))

                    # Заполняем таблицы:
                    self.fill_info(event)

                elif queued.before_notification > 0:
                    queued.before_notification -= 1
                    self.session.commit()
                elif queued.before_notification == 0:
                    queued.before_notification -= 1
                    self.session.commit()
                    self.VkApi.message_send(peer_id,
                                            message_loader('no_admin_permissions.txt'))
            else:
                cu = self.session.query(ConferenceUser).filter(ConferenceUser.conference_id == peer_id,
                                                               ConferenceUser.user_id == message_object[
                                                                   'from_id']).first()
                print(cu)

    def chat_action(self, message_object):
        action = message_object['action']
        if action['type'] == 'chat_invite_user':
            if action['member_id'] == -194017842:
                self.invite_in_chat(message_object)

        elif action['type'] == 'chat_kick_user':
            print('Сдох челик...')
        elif action['type'] == 'chat_photo_update':
            pass
        elif action['type'] == 'chat_title_update':
            pass
        elif action['type'] == 'chat_photo_remove':
            pass
        elif action['type'] == 'chat_photo_update':
            pass
        else:
            print(message_object)
            print('Непонятное действие!')

    def invite_in_chat(self, message_object):
        self.VkApi.message_send(message_object['peer_id'],
                                message_loader('invite_in_conference.txt'),
                                photo_loader('hello_god'))

        conferences_queue = ConferencesQueue()
        conferences_queue.conference_id = message_object['peer_id']
        self.session.add(conferences_queue)
        self.session.commit()

    def fill_info(self, event):
        message_object = event.obj.message
        peer_id = message_object['peer_id']

        conference_info = self.VkApi.get_conference_info(peer_id)
        members_info = self.VkApi.get_members(peer_id)
        print(conference_info)
        new_conference = Conference()
        new_conference.conference_id = peer_id
        new_conference.owner = conference_info['chat_settings']['owner_id']
        new_conference.title = conference_info['chat_settings']['title']
        new_conference.photo = conference_info['chat_settings']['photo']['photo_200']
        new_conference.pinned_message_id = conference_info['chat_settings']['pinned_message'][
            'conversation_message_id']
        self.session.add(new_conference)
        self.session.commit()

        for member in members_info['profiles']:
            conference_user = ConferenceUser()
            user = User()

            user.user_id = member['id']
            user.name = member['first_name']
            user.surname = member['last_name']
            user.sex = member['sex']
            user.is_closed = member['is_closed']
            user.conferences.append(new_conference)
            self.session.add(user)

            conference_user.user_id = member['id']
            conference_user.conference_id = peer_id
            conference_user.invited_by, \
            conference_user.is_admin, \
            conference_user.is_owner, \
            conference_user.join_date = find_member_info(member['id'], members_info['items'])

            if conference_user.is_admin:
                conference_user.kick = True
                conference_user.warn = True

            new_conference.members.append(user)
            self.session.add(conference_user)
            self.session.commit()

    def update_conference_members(self, peer_id):
        conference_info = self.VkApi.get_conference_info(peer_id)
        members_info = self.VkApi.get_members(peer_id)

        for member in members_info['profiles']:
            user = self.session.query(User).filter(User.user_id == member['id'])
            conference = self.session.query(Conference).filter(Conference.conference_id == peer_id)
            conference_user = self.session.query(ConferenceUser).filter(ConferenceUser.conference_id == peer_id,
                                                                        ConferenceUser.user_id == member['id'])



if __name__ == '__main__':
    GodBotVk().start_pooling()
