from .Api import Vk

vk = Vk()


class GodBotVk:
    def __init__(self):
        for event in vk.LongPool.listen():
            print(event)
