from time import sleep

from bot.bot import GodBotVk
from panel.data.models.all_conferences import Conference


def update(gb):
    confs = [conf.conference_id for conf in gb.session.query(Conference).all()]
    [gb.update_conference_messages(i) for i in confs]


def updater():
    print('Updating is starting')
    gb = GodBotVk()
    while True:
        update(gb)
        sleep(5)
