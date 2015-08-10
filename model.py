__author__ = 'pknox-kennedy'

import json

def to_json(python_object):
    if isinstance(python_object,sound):
        return {"__class__":'sound',
                'filename': python_object.filename}

def from_json(json_object):
    if '__class__' in json_object:
        if json_object['__class__'] == 'sound':
            return sound(json_object['filename'])

class sound():
    def __init__(self, filename):
        self.filename = filename



class show():

    def __init__(self):
        self.items = []
        self._loaded = False

    def load(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            self.items = json.load(f, object_hook=from_json)
        self._loaded = True

    def save(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.items, f, default=to_json)

if __name__ == '__main__':
    s1 = show()
    s1.items.append(sound('scream'))
    s1.items.append(sound('lightning'))
    s1.save('bob.json')
    s1.load('bob.json')
    print(s1.items)
