from flask_restful import Api,Resource
from flask import request
import sys,os,json

sys.path.append(os.getcwd() + '/common')
from Auth import Auth
from MysqlHandle import MysqlHandle

# 获取机器详情
class MachineDetail(Resource, Auth, MysqlHandle):
    def __init__(self):
        Auth.__init__(self)

    def get(self, machId):
        data = MysqlHandle().getOneDockerByUserIdAndDockerId(self.userId, machId)
        return {'code': 200, 'msg': 'success', 'data': self.formatData(data)}

    def formatData(self, data):
        if ('db_info' not in data):
            return {}
        res = json.loads(data['db_info'])
        return res

# 获取分配给用户的机器列表
class MachineList(Resource, Auth, MysqlHandle):
    def __init__(self):
        Auth.__init__(self)

    def get(self, machType = 1):
        data = MysqlHandle().getAllDockersByUserId(self.userId, machType)
        return {'code': 200, 'msg': 'success', 'data': self.formatData(data)}

    def formatData(self, data):
        if (len(data) == 0):
            return data
        res = []
        for v in data:
            res.append(json.loads(v['db_info']))
        return res
