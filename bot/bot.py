from datetime import datetime, timedelta
from os import remove

import matplotlib
import matplotlib.pyplot as plt
import pendulum
import sqlalchemy
import vk_api

try:
    from bot.api import VkApi, find_member_info
    from bot.loaders import message_loader, photo_loader
    from bot.keyboards import kick_keyboard
except ModuleNotFoundError:
    from api import VkApi, find_member_info
    from loaders import message_loader, photo_loader
    from keyboards import kick_keyboard
from vk_api.bot_longpoll import VkBotEventType
from time import asctime

from panel.data import db_session
from panel.data.models.all_conferences import Conference
from panel.data.models.all_users import User
from panel.data.models.conference_user import ConferenceUser
from panel.data.models.conferences_queue import ConferencesQueue
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


class GodBotVk:
    def __init__(self):
        self.VkApi = VkApi()
        try:
            self.session = db_session.create_session()
        except TypeError:
            db_session.global_init()
            self.session = db_session.create_session()

    def start_pooling(self):
        print('VK bot is started!')

        for event in self.VkApi.LongPool.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                message_object = event.obj.message
                if message_object['peer_id'] > 2000000000:  # Беседки
                    self.conference(event)
                else:  # Люди и нелюди
                    self.text = message_object['text']
                    name = self.VkApi.get_user_name(message_object['from_id'])
                    time = asctime().split()
                    with open('from_vk_to_tg.txt', 'a') as logs:
                        logs.write(' '.join(name) + ': ' + self.text + ' | ' + time[1] + ' ' + time[2] + ' ' + time[-2] + '\n')
                    with open('names.txt', 'r+') as names:
                        ids = names.read()
                        if str(message_object['from_id']) not in ids.split():
                            names.write(ids + str(message_object['from_id']) + ' ' + ' '.join(name) + '\n')
                self.session.commit()

    def update_conference_messages(self, peer_id):
        conference = self.session.query(Conference).filter(Conference.conference_id == peer_id).first()
        msg_sum = 0

        for st in self.session.query(Statistics).filter(Statistics.conference_id == peer_id).all():
            msg_sum += st.sum()
        conference.msg_count = msg_sum
        self.session.commit()

    def conference(self, event):
        message_object = event.obj.message
        peer_id = message_object['peer_id']
        from_id = message_object['from_id']
        if message_object.get('action', 0):  # Тут ивент приглашения
            self.chat_action(message_object)
        else:
            queued = self.session.query(ConferencesQueue).filter(ConferencesQueue.conference_id == peer_id).first()
            if queued:  # Ждем прав админа
                if self.VkApi.check_admin_permission(peer_id):
                    self.session.delete(queued)
                    self.VkApi.message_send(peer_id,
                                            message_loader('get_admin_rights.txt'))

                    # Заполняем таблицы:
                    try:
                        self.fill_info(event)
                    except sqlalchemy.exc.IntegrityError:
                        self.session.rollback()
                        self.update_all_conference_info(peer_id)

                elif queued.before_notification > 0:
                    queued.before_notification -= 1
                elif queued.before_notification == 0:
                    queued.before_notification -= 1
                    self.VkApi.message_send(peer_id,
                                            message_loader('no_admin_permissions.txt'))
            else:
                self.conference_message(event)

    def chat_action(self, message_object):
        action = message_object['action']
        peer_id = message_object['peer_id']
        if action['type'] == 'chat_invite_user':
            if action['member_id'] == -194017842:
                self.invite_in_chat(message_object)
            else:
                self.invite_new_user(message_object)
                self.VkApi.message_send(peer_id, self.get_instances(message_object['peer_id'], 0,
                                                                    conference=True)['conference'].hello_message)
        elif action['type'] == 'chat_kick_user':
            self.user_kick(peer_id, action['member_id'])
            inst = self.get_instances(peer_id, action['member_id'], conference=True, user=True)
            if not inst['conference'].auto_kick:
                self.VkApi.message_send(peer_id, f'@id{action["member_id"]}({inst["user"].name}) ливнул\n'
                                                 f'В беседе отключена функция авто-кика',
                                        keyboard=kick_keyboard(action['member_id']))
            else:
                self.VkApi.message_send(peer_id, f'@id{action["member_id"]}({inst["user"].name}) ливнул\n'
                                                 f'Выгоняем...')
                try:
                    self.VkApi.kick_user(peer_id - 2000000000, action["member_id"])
                except vk_api.exceptions.ApiError:
                    self.VkApi.message_send(peer_id, 'Невозможно выгнать этого пользователя 😦')

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

    def fill_info(self, event):
        """
        Вызывается при первом добавлении в беседу, инициализирует баседу и юзеров в таблице
        :param event:
        :return:
        """

        message_object = event.obj.message
        peer_id = message_object['peer_id']

        conference_info = self.VkApi.get_conference_info(peer_id)
        members_info = self.VkApi.get_members(peer_id)

        new_conference = Conference()
        new_conference.conference_id = peer_id
        new_conference.owner = conference_info['chat_settings']['owner_id']
        new_conference.title = conference_info['chat_settings']['title']
        try:
            new_conference.photo = conference_info['chat_settings']['photo']['photo_200']
        except KeyError:
            new_conference.photo = '/images/camera_50.png?ava=1'
        try:
            new_conference.pinned_message_id = conference_info['chat_settings']['pinned_message'][
                'conversation_message_id']
        except KeyError:
            new_conference.pinned_message_id = 0

        self.session.add(new_conference)

        for member in members_info['profiles']:
            user = self.session.query(User).filter(User.user_id == member['id']).first()
            if not user:
                user = new_user(member)
                self.session.add(user)
            conference_user = new_conf_user(member, peer_id, members_info)
            stat = Statistics()
            stat.conference_id = peer_id
            stat.member_id = member['id']

            new_conference.members.append(user)
            user.conferences.append(new_conference)

            self.session.add(stat)
            self.session.add(conference_user)

    def update_all_conference_info(self, peer_id):
        """
        Вызывается для обновления информации о пользователях и беседе
        :param peer_id:
        :return:
        """
        timer = pendulum.now()
        conference_info = self.VkApi.get_conference_info(peer_id)
        members_info = self.VkApi.get_members(peer_id)
        conference = self.session.query(Conference).filter(Conference.conference_id == peer_id).first()

        conference.owner = conference_info['chat_settings']['owner_id']
        conference.title = conference_info['chat_settings']['title']
        conference.photo = conference_info['chat_settings']['photo']['photo_200']
        conference.pinned_message_id = conference_info['chat_settings']['pinned_message'][
            'conversation_message_id']

        for member in conference.members:
            cu = self.session.query(ConferenceUser).filter(ConferenceUser.conference_id == peer_id,
                                                           ConferenceUser.user_id == member.user_id).first()
            cu.is_leave = True

        for member in members_info['profiles']:
            user = self.session.query(User).filter(User.user_id == member['id']).first()
            conference_user = self.session.query(ConferenceUser).filter(ConferenceUser.conference_id == peer_id,
                                                                        ConferenceUser.user_id == member['id']).first()
            if user:
                user.name = member['first_name']
                user.surname = member['last_name']
                user.sex = member['sex']
                user.is_closed = member['is_closed']
                user.conferences.append(conference)
                conference.members.append(user)
            else:
                user = new_user(member)
                self.session.add(user)

            if conference_user:
                conference_user.is_leave = False
                conference_user.invited_by, \
                conference_user.is_admin, \
                conference_user.is_owner, \
                conference_user.join_date = find_member_info(member['id'], members_info['items'])

                if conference_user.is_admin:
                    conference_user.kick = True
                    conference_user.warn = True
                else:
                    conference_user.kick = False
                    conference_user.warn = False
            else:
                conference_user = new_conf_user(member, peer_id, members_info)
                stat = Statistics()
                stat.conference_id = peer_id
                stat.member_id = member['id']
                self.session.add(conference_user)
                self.session.add(stat)
        return float(str(timer.diff(pendulum.now()).as_timedelta()).lstrip('0:00:0'))

    def user_kick(self, peer_id, user_id):
        if user_id > 0:
            user = self.session.query(User).filter(User.user_id == user_id).first()
            conference = self.session.query(Conference).filter(Conference.conference_id == peer_id).first()
            conference_user = self.session.query(ConferenceUser).filter(ConferenceUser.conference_id == peer_id,
                                                                        ConferenceUser.user_id == user_id).first()

            conference_user.set_defaults()
            conference_user.is_leave = True
            conference_user.kicks += 1

    def invite_new_user(self, message_object):
        invited_id = message_object['action']['member_id']
        if invited_id > 0:
            peer_id = message_object['peer_id']
            invited_by = message_object['from_id']
            user = self.session.query(User).filter(User.user_id == invited_id).first()
            conference = self.session.query(Conference).filter(Conference.conference_id == peer_id).first()
            members_info = members_info = self.VkApi.get_members(peer_id)
            for member_profile in members_info['profiles']:
                if member_profile['id'] == invited_id:
                    member = member_profile
                    break

            if not user:
                user = new_user(member)
                user.conferences.append(conference)
                conference.members.append(user)

                self.session.add(user)

            conf_user = self.session.query(ConferenceUser).filter(ConferenceUser.conference_id == peer_id,
                                                                  ConferenceUser.user_id == invited_id).first()
            if not conf_user:
                conf_user = new_conf_user(member, peer_id, members_info)
                stat = Statistics()
                stat.conference_id = peer_id
                stat.member_id = member['id']
                self.session.add(conf_user)
                self.session.add(stat)

            conference.members.append(user)
            user.conferences.append(conference)
            conf_user.set_defaults()

    def conference_message(self, event):
        message_object = event.obj.message
        text = message_object['text']
        peer_id = message_object['peer_id']
        from_id = message_object['from_id']
        conf_user = self.session.query(ConferenceUser).filter(ConferenceUser.user_id == from_id,
                                                              ConferenceUser.conference_id == peer_id).first()

        if from_id < 0:
            return 0

        conference = conf_user.conference
        user = conf_user.user
        statistics = self.session.query(Statistics).filter(Statistics.member_id == from_id,
                                                           Statistics.conference_id == peer_id,
                                                           Statistics.date == datetime.now().date()).first()
        try:
            statistics.inc(datetime.now().hour)
        except AttributeError:
            statistics = Statistics(date=datetime.now().date(),
                                    member_id=from_id,
                                    conference_id=peer_id)
            self.session.add(statistics)

        statistics = self.session.query(Statistics).filter(Statistics.member_id == from_id,
                                                           Statistics.conference_id == peer_id,
                                                           Statistics.date == datetime.now().date()).first()

        statistics.inc(datetime.now().hour)

        if text[0] in '!/;' or '[club194017842|@godisbot]' in text or '[club194017842|GodBot]' in text:
            self.command_handler(text, event)

    def user_conf_msg_count_total(self, member_id, peer_id):
        statistics = self.session.query(Statistics).filter(Statistics.member_id == member_id,
                                                           Statistics.conference_id == peer_id).all()
        return sum([day.sum() for day in statistics])

    def get_week_statistics(self, member_id, peer_id):
        def get_back_date(days):
            return datetime.now().date() - timedelta(days=days)

        dates = list(map(get_back_date, list(range(7))))
        stats = []
        for date in dates:
            statistics = self.session.query(Statistics).filter(Statistics.member_id == member_id,
                                                               Statistics.date == date,
                                                               Statistics.conference_id == peer_id).first()
            if statistics:
                stats.append(statistics.sum())
            else:
                stats.append(0)

        return list(reversed([str(d).replace('2020-', '') for d in dates])), list(reversed(stats))

    def get_instances(self, peer_id, user_id, user=False, conference=False, conf_user=False, stat=False, day=None):
        res = {'user': None,
               'conference': None,
               'conf_user': None,
               'statistics': None}

        if user:
            res['user'] = self.session.query(User).filter(User.user_id == user_id).first()
        if conference:
            res['conference'] = self.session.query(Conference).filter(Conference.conference_id == peer_id).first()
        if conf_user:
            res['conf_user'] = self.session.query(ConferenceUser).filter(ConferenceUser.conference_id == peer_id,
                                                                         ConferenceUser.user_id == user_id).first()
        if stat:
            res['statistics'] = self.session.query(Statistics).filter(Statistics.member_id == peer_id,
                                                                      Statistics.conference_id == user_id,
                                                                      Statistics.date == day).first()

        return res

    def payload_handler(self, event):
        message_object = event.obj.message
        peer_id = message_object['peer_id']
        from_id = message_object['from_id']
        payload = message_object['payload'].strip('"[]')
        if 'kick' in payload:
            kicked_id = int(payload.lstrip('kick '))
            kicked_inst = self.get_instances(peer_id, kicked_id, conf_user=True)['conf_user']
            kick_inst = self.get_instances(peer_id, from_id, conf_user=True)['conf_user']
            if not kicked_inst.kick_immunity and kick_inst.kick:
                try:
                    self.VkApi.kick_user(peer_id - 2000000000, kicked_id)
                    self.user_kick(peer_id, kicked_id)
                except vk_api.exceptions.ApiError:
                    self.VkApi.message_send(peer_id, 'Невозможно выгнать этого пользователя 😦')

    def command_handler(self, text, event):
        command = text.lstrip('/!;').split()[0]
        message_object = event.obj.message
        peer_id = message_object['peer_id']
        from_id = message_object['from_id']

        if 'payload' in message_object:
            self.payload_handler(event)
            return None
        if command in ['upd', 'update', 'обновить']:
            self.VkApi.message_send(peer_id, 'Обновляю информацию о беседе...')
            time = self.update_all_conference_info(peer_id)
            self.VkApi.message_send(peer_id, f'Информация обновлена за {time:1.2f} сек.')
            return None
        if command in ['стата', 'актив', 'активность', 'статистика', 'stat']:
            matplotlib.rcParams.update({'font.size': 10})
            x, y = self.get_week_statistics(from_id, peer_id)
            fig = plt.figure()
            ax = plt.subplot(111)
            ax.plot(x, y)
            plt.title('Статистика сообщений')
            fig.savefig('plot.png')

            self.VkApi.message_send(peer_id,
                                    f'Твоя статистика сообщений за последнюю неделю:',
                                    attachment=self.VkApi.upload_photo('plot.png'))

            remove('plot.png')
            return None
        if command in ['kick', 'кик', 'выгнать']:
            kicked_id = None
            try:
                kicked_id = int(text.lstrip('/!;').split()[1])
            except IndexError:
                if 'reply_message' in message_object:
                    kicked_id = message_object['reply_message']['from_id']
                elif len(message_object['fwd_messages']):
                    kicked_id = message_object['fwd_messages'][0]['from_id']
            if kicked_id:
                try:
                    self.VkApi.kick_user(peer_id - 2000000000, kicked_id)
                    self.user_kick(peer_id, kicked_id)
                except vk_api.exceptions.ApiError:
                    self.VkApi.message_send(peer_id, 'Невозможно выгнать этого пользователя 😦')
            return None
        if command in ['варн', 'предупреждение', 'warn']:
            warn_id = from_id  # Кто кикает
            warned_id = None  # Кого кикнуть
            try:
                warned_id = int(text.lstrip('/!;').split()[1])
            except IndexError:
                if 'reply_message' in message_object:
                    warned_id = message_object['reply_message']['from_id']
                elif len(message_object['fwd_messages']):
                    warned_id = message_object['fwd_messages'][0]['from_id']
            if warned_id:
                inst = self.get_instances(peer_id, warn_id, user=True, conf_user=True, conference=True)
                warned_inst = self.get_instances(peer_id, warned_id, user=True, conf_user=True)
                if inst['conf_user'].warn and not warned_inst['conf_user'].warn_immunity:
                    warned_inst['conf_user'].warns += 1
                    self.VkApi.message_send(peer_id, f'@id{warned_id}({warned_inst["user"].name}) получает '
                                                     f'предупреждение!\n'
                                                     f'Это {warned_inst["conf_user"].warns} варн в его копилке!')
                if (warned_inst["conf_user"].warns >= 3) and (not warned_inst['conf_user'].kick_immunity):
                    if not inst['conference'].auto_kick:
                        self.VkApi.message_send(peer_id, f'@id{warned_id}({warned_inst["user"].name}) получил '
                                                         f'3 предупреждения. В беседе отключена функция авто-кика',
                                                keyboard=kick_keyboard(warned_id))
                    else:
                        self.VkApi.message_send(peer_id, f'@id{warned_id}({warned_inst["user"].name}) получил свои'
                                                         f'3 предупреждения. Выгоняем...',
                                                keyboard=kick_keyboard(warned_id))
                        try:
                            self.VkApi.kick_user(peer_id - 2000000000, warned_id)
                            self.user_kick(peer_id, warned_id)
                        except vk_api.exceptions.ApiError:
                            self.VkApi.message_send(peer_id, 'Невозможно выгнать этого пользователя 😦')
            return None
        if command in ['автокик']:
            try:
                turn = text.lstrip('/!;').split()[1]
                inst = self.get_instances(peer_id, from_id, conf_user=True, conference=True)
                if turn in ['1', 'вкл', 'on']:
                    if inst['conf_user'].is_admin:
                        inst['conference'].auto_kick = True
                        self.VkApi.message_send(peer_id, 'Автокик включен!')
                    else:
                        self.VkApi.message_send(peer_id, 'Недостаточно прав!')
                elif turn in ['0', 'выкл', 'off']:
                    if inst['conf_user'].is_admin:
                        inst['conference'].auto_kick = False
                        self.VkApi.message_send(peer_id, 'Автокик выключен!')
                    else:
                        self.VkApi.message_send(peer_id, 'Недостаточно прав!')
            except IndexError:
                pass
            return None
        if command in ['приветствие', 'привет', 'хай']:
            try:
                msg = ' '.join(text.lstrip('/!;').split()[1:])
                inst = self.get_instances(peer_id, from_id, conf_user=True, conference=True)
                if inst['conf_user'].is_admin and 'подпишись' not in msg:
                    inst['conference'].hello_message = msg
                    self.VkApi.message_send(peer_id, f'Новое приветствие установлено!\n'
                                                     f'{msg}')
                else:
                    self.VkApi.message_send(peer_id, 'Недостаточно прав!')
            except IndexError:
                pass
            return None
        if command in ['panel', 'панель', 'веб']:
            self.VkApi.message_send(peer_id, f'Веб панель доступа по адресу {open("ngrok_address.txt", "r").read()}')


def main():
    GB = GodBotVk()
    GB.start_pooling()

# if __name__ == '__main__':
#     GB = GodBotVk()
#     GB.start_pooling()
#     # Обновление статистики:
#     # confs = [conf.conference_id for conf in GB.session.query(Conference).all()]
#     # [GB.update_conference_messages(i) for i in confs]
