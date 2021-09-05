from flask import Flask
import os,sys
from flask_restful import Api,Resource
sys.path.append(os.getcwd() + '/api')
from Machine import MachineDetail,MachineList
from MysqlMachine import MysqlMachine
from RedisMachine import RedisMachine

app = Flask(__name__)

if __name__ == '__main__':
    api = Api(app)
    api.add_resource(MysqlMachine, '/mysql')
    api.add_resource(RedisMachine, '/redis')
    api.add_resource(MachineList, '/list/<int:machType>')
    api.add_resource(MachineDetail, '/detail/<string:machId>')
    app.run()
