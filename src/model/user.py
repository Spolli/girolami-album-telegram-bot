import json

class User:
    def __init__(self, index, name, id):
        self.index = index
        self.name = name
        self.id = id
    
    def to_json(self):
        return json.dump({'index': self.index, 'name': self.name, 'id': self.id}, f, ensure_ascii=False, indent=4)
    
    def from_json(js):
        usr = json.loads(js)
        return User(usr['index'], usr['name'], usr['id'])