from flask import request

# 鉴权类
class Auth():
    def __init__(self):
        auth = request.headers.get('Authorization')
        self.userList = {"user1": 1, "user2": 2, "user3": 3}
        self.authStatus = False
        self.userId = -1
        if auth in self.userList:
            self.authStatus = True
            self.userId = self.userList[auth]
