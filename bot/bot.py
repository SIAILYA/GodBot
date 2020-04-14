from tools.api import VkApi
from tools.loaders import message_loader, photo_loader
from tools.other import event_pprint
from vk_api.bot_longpoll import VkBotEventType

from panel.data import db_session
from panel.data.db_session import create_session
from panel.data.models.conferences_queue import ConferencesQueue


# TODO: При приглашении в беседу:
#  1. При успехе спарсить все данные и записать таблицы


class GodBotVk:
    def __init__(self):
        self.VkApi = VkApi()
        try:
            self.session = create_session()
        except TypeError:
            db_session.global_init()
            self.session = create_session()

    def start_pooling(self):
        for event in self.VkApi.LongPool.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                print('=====================')
                event_pprint(event)
                print('=====================')

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
                    self.VkApi.get_conference_info(peer_id)  # TODO: Сделать все через execute запрос, заполнить данные

                elif queued.before_notification > 0:
                    queued.before_notification -= 1
                    self.session.commit()
                elif queued.before_notification == 0:
                    queued.before_notification -= 1
                    self.session.commit()
                    self.VkApi.message_send(peer_id,
                                            message_loader('no_admin_permissions.txt'))
            else:
                self.VkApi.get_conference_info(peer_id)

    def chat_action(self, message_object):
        action = message_object['action']
        if action['type'] == 'chat_invite_user':
            if action['member_id'] == -194017842:
                self.VkApi.message_send(message_object['peer_id'],
                                        message_loader('invite_in_conference.txt'),
                                        photo_loader('hello_god'))

                conferences_queue = ConferencesQueue()
                conferences_queue.conference_id = message_object['peer_id']
                self.session.add(conferences_queue)
                self.session.commit()

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


if __name__ == '__main__':
    GodBotVk().start_pooling()
