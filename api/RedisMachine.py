from flask_restful import Api,Resource
from flask import request
import sys,os

sys.path.append(os.getcwd() + '/common')
from Auth import Auth
from MysqlHandle import MysqlHandle

sys.path.append(os.getcwd() + '/service')
from DockerSvr import DockerSvr

# 获取redis
class RedisMachine(Resource, Auth, DockerSvr):
    def __init__(self):
        Auth.__init__(self)

    def post(self):
        if (self.authStatus == False):
            return {'code': 403}
        params = request.get_json()
        memory = 500
        if 'memory' in params:
            memory = params['memory']
        res, info = DockerSvr().createRedis(self.userId, memory)
        if (res == True):
            return {'code': 200, 'msg': 'success', 'data': info}
        return {'code': 500, 'msg': 'server error, please retry!', 'data':'{}'}
