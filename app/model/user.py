class User:
    def __init__(self, user_id, name, photo):
        self._id = user_id
        self._name = name
        self._photo = photo
    
    @staticmethod
    def from_vk_json(json):
        return User(json['id'],
                    "{} {}".format(json['first_name'], json['last_name']),
                    json['photo_200_orig'])
    
    @staticmethod
    def from_json(json):
        return User(json['id'], json['name'], json['photo'])
    
    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name
    
    @property
    def photo(self):
        return self._photo
