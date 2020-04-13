import vk_api.vk_api
from vk_api import VkUpload
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.utils import get_random_id


class Vk:  # TODO: Привести этот АПИ в нормальный вид
    def __init__(self):
        self.VkSession = vk_api.VkApi(
            token='e9c4bbb6d86e3115e0bbcb10bfe18ef57bb0c027500562e6c187fccea82c91e98cedb62818fd4d1c90d46')
        self.VkApi = self.VkSession.get_api()
        self.LongPool = VkBotLongPoll(self.VkSession, group_id='194017842')

    def MessageSend(self, send_id, message=None, attachment=None, keyboard=None):
        self.VkApi.messages.send(peer_id=send_id,
                                 message=message,
                                 random_id=get_random_id(),
                                 attachment=attachment,
                                 keyboard=keyboard)

    def CheckOnline(self, user_id):
        info = self.VkApi.users.get(user_ids=user_id, fields=['online'])
        return info

    def ConsoleMessage(self, message):
        self.MessageSend('', message)

    def UploadAttachmentPhoto(self, photo):
        upload = VkUpload(self.VkSession)
        response = upload.photo_messages(photo)[0]
        return f'photo{response["owner_id"]}_{response["id"]}_{response["access_key"]}'

    def UserNameGet(self, user_id):
        info = self.VkApi.users.get(user_ids=user_id)[0]
        return info['first_name'], info['last_name']

    def SetActivity(self, peer_id):
        self.VkApi.messages.setActivity(type='typing',
                                        peer_id=peer_id,
                                        group_id='')

    def ManyMessagesSend(self, user_ids, message=None, attachment=None, keyboard=None):
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


if __name__ == '__main__':
    VkSession = vk_api.VkApi(
        token='e9c4bbb6d86e3115e0bbcb10bfe18ef57bb0c027500562e6c187fccea82c91e98cedb62818fd4d1c90d46')
    VkApi = VkSession.get_api()
    print(VkApi.messages.getConversationsById(peer_ids=2000000001, group_id=194017842))
