import vk_api.vk_api
from vk_api import VkUpload
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id


class VkApi:
    def __init__(self):
        self.VkSession = vk_api.VkApi(
            token='e9c4bbb6d86e3115e0bbcb10bfe18ef57bb0c027500562e6c187fccea82c91e98cedb62818fd4d1c90d46')
        self.VkApi = self.VkSession.get_api()
        self.LongPool = VkBotLongPoll(self.VkSession, group_id='194017842')

    def message_send(self, send_id, message=None, attachment=None, keyboard=None):
        self.VkApi.messages.send(peer_id=send_id,
                                 message=message,
                                 random_id=get_random_id(),
                                 attachment=attachment,
                                 keyboard=keyboard)

    def check_online(self, user_id):
        info = self.VkApi.users.get(user_ids=user_id, fields=['online'])
        return info

    def upload_photo(self, photo):
        upload = VkUpload(self.VkSession)
        response = upload.photo_messages(photo)[0]
        return f'photo{response["owner_id"]}_{response["id"]}_{response["access_key"]}'

    def get_user_name(self, user_id):
        info = self.VkApi.users.get(user_ids=user_id)[0]
        return info['first_name'], info['last_name']

    def set_activity_typing(self, peer_id):
        self.VkApi.messages.setActivity(type='typing',
                                        peer_id=peer_id,
                                        group_id='')

    def check_admin_permission(self, peer_id):
        conf_info = self.VkApi.messages.getConversationsById(peer_ids=peer_id, group_id=194017842)
        if not conf_info['count']:
            return False
        return True

    def get_members(self, peer_id):
        conf_members = self.VkApi.messages.getConversationMembers(peer_id=peer_id, group_id=194017842)
        return conf_members

    def get_conference_info(self, peer_id):
        conf_info = self.VkApi.messages.getConversationsById(peer_ids=peer_id, group_id=194017842)
        return conf_info['items'][0]

    def distribution(self, user_ids, message=None, attachment=None, keyboard=None):
        if len(user_ids) > 100:
            for i in range(len(user_ids) // 100 + 1):
                self.VkApi.messages.send(user_ids=user_ids[i * 100: 100 * (i + 1)],
                                         message=message,
                                         random_id=get_random_id(),
                                         attachment=attachment,
                                         keyboard=keyboard)
        else:
            self.VkApi.messages.send(user_ids=user_ids,
                                     message=message,
                                     random_id=get_random_id(),
                                     attachment=attachment,
                                     keyboard=keyboard)


def find_member_info(member_id, items):
    for i in items:
        if i['member_id'] == member_id:
            return i['invited_by'], i.get('is_admin', False), i.get('is_owner', False), i.get('join_date', None)
