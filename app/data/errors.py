class DBError(Exception):
    pass

class Missing(DBError):
    def __init__(self, msg:str):
        super().__init__(f"Not found name: {msg}")
        self.msg = msg

class Duplicate(DBError):
    def __init__(self, msg:str):
        super().__init__(f"The name: {msg} exists")
        self.msg = msg