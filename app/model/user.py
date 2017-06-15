class User:
    def __init__(self, user_id, first_name, last_name, photo, domain):
        self._id = user_id
        self._first_name = first_name
        self._last_name = last_name
        self._photo = photo
        self._domain = domain
        self._color = None
    
    @staticmethod
    def from_vk_json(json):
        return User(json['id'],
                    json['first_name'], json['last_name'],
                    json['photo_100'], json['domain'])
    
    def to_json(self):
        return dict(id=self.id, name=self.name, photo=self.photo,
                    link=self.link, color=self.color)
    
    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return "{} {}".format(self._first_name, self._last_name)
    
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
