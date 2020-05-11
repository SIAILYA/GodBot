import json


def message_loader(file):
    with open(f'C:/Projects/GodBot/bot/messages_presets/{file}', encoding='u8') as msg_file:
        return msg_file.read()


def photo_loader(photo):
    photos = json.loads(open(r'C:\Projects\GodBot\bot\messages_presets\uploaded_photos.json', encoding='u8').read())
    return photos[photo]
