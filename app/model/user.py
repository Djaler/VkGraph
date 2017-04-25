class User:
    def __init__(self, id, first_name, last_name, photo=""):
        self._id = id
        self._first_name = first_name
        self._last_name = last_name
        self._photo = photo
    
    @staticmethod
    def from_json(json):
        return User(json['id'], json['first_name'], json['last_name'],
                    json['photo_200_orig'])
    
    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return "{} {}".format(self._first_name, self._last_name)
    
    @property
    def photo(self):
        return self._photo