class User:
    def __init__(self, user_id, name, photo, domain):
        self._id = user_id
        self._name = name
        self._photo = photo
        self._domain = domain
        self._color = ""
    
    @staticmethod
    def from_vk_json(json):
        return User(json['id'],
                    "{} {}".format(json['first_name'], json['last_name']),
                    json['photo_100'], json['domain'])
    
    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name
    
    @property
    def photo(self):
        return self._photo
    
    @property
    def link(self):
        return "https://vk.com/{}".format(self._domain)
    
    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, value):
        self._color = value
