import json


def event_pprint(event, other=False):
    if other:
        print(json.dumps(json.loads(str(event).replace("'", '"').replace('True', '"True"').replace('False', '"False"')),
                         indent=4, sort_keys=True))
    else:
        print(json.dumps(
            json.loads(str(event.obj).replace("'", '"').replace('True', '"True"').replace('False', '"False"')),
            indent=4, sort_keys=True))
