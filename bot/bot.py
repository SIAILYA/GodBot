from .Api import Vk

vk = Vk()


# TODO: При приглашении в беседу:
#  1. Получить всю информацию о беседе (желательно в 1 запрос (мб через execute)) -
#  название, юзеры в беседе, админ
#  2. Записать все по таблицам - добавить всю информацию о пользователях


class GodBotVk:
    def __init__(self):
        for event in vk.LongPool.listen():
            print(event)
