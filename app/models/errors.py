class UserError(Exception):
    pass

class UserNameError(UserError):
    def __init__(self,msg:str):
        self.msg = msg