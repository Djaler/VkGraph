class Status:
    OK = "OK"
    ERROR = "ERROR"


class Response(dict):
    def __init__(self, status, data):
        super().__init__()
        
        self["status"] = status
        self["data"] = data
