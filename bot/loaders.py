import json


def message_loader(file):
    with open(f'messages_presets/{file}', encoding='u8') as msg_file:
        return msg_file.read()


def photo_loader(photo):
    photos = json.loads(open('messages_presets/uploaded_photos.json', encoding='u8').read())
    return photos[photo]
