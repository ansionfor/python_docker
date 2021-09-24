import subprocess,socket,random,json,sys,os

sys.path.append(os.getcwd() + '/common')
from MysqlHandle import MysqlHandle

# docker操作svr
class DockerSvr(MysqlHandle):
    def __init__(self):
        return

    def createMysql(self, userId, charset="utf8", collation="utf8_general_ci"):
        # 获取可用端口号
        newPort = self.getNewPort()
        if (newPort == False):
            print('get new port fail', userId)
            return False, {}

        pwd = random.randint(10000000,99999999)
        userName = "mysql-{}".format(newPort)
        shell = (
        "docker run -itd --name {} -p {}:3306 -e MYSQL_ROOT_PASSWORD={} mysql:8.0 "
        "--character-set-server={} --collation-server={} --default-authentication-plugin=mysql_native_password"
        ).format(userName, newPort, pwd, charset, collation)

        # 创建docker
        res = subprocess.run(shell, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout = str(res.stdout.decode("utf-8"))
        if (len(stdout) != 65):
            print('create docker fail', userId, stdout)
            return False, {}
        dockerId = stdout[0:12]

        # 判断是否创建成功
        if (self.isDockerExist(dockerId) == False):
            print('docker exist', userId, dockerId)
            return False, {}

        # 入库
        info = {}
        info['host'] = '127.0.0.1'
        info['user'] = 'root'
        info['pwd'] = pwd
        info['port'] = newPort
        info['dockerId'] = dockerId
        res = MysqlHandle().insertDocker(userId, dockerId, 1, json.dumps(info), newPort)
        if (res == False):
            print('insert docker to db fail', userId, info)
            return False, {}
        return True, info

    # 创建redis实例，memory：内存容量（M）
    def createRedis(self, userId, memory=500):
        # 获取可用端口号
        newPort = self.getNewPort()
        if (newPort == False):
            print('get new port fail', userId)
            return False, {}

        pwd = random.randint(10000000,99999999)
        userName = "redis-{}".format(newPort) 
        shell = (
        "docker run -itd -m {}M --name redis-{} -p {}:6379 redis:5.0 --requirepass {}"
        ).format(memory, userName, newPort, pwd)

        # 创建docker
        res = subprocess.run(shell, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout = str(res.stdout.decode("utf-8"))
        if (len(stdout) != 65):
            print('create docker fail', userId, stdout)
            return False, {}

        # 判断是否创建成功
        dockerId = stdout[0:12]  
        if (self.isDockerExist(dockerId) == False):
            print('docker exist', userId, stdout)
            return False, {}

        # 入库
        info = {}
        info['host'] = '127.0.0.1'
        info['pwd'] = pwd
        info['port'] = newPort
        info['dockerId'] = dockerId
        res = MysqlHandle().insertDocker(userId, dockerId, 2, json.dumps(info), newPort)
        if (res == False):
            print('insert docker to db fail', userId, info)
            return False, {}
        return True, info

    # 判断docker是否正在运行
    def isDockerExist(self, dockerId):
        shell = "docker ps"
        res = subprocess.run(shell, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout = str(res.stdout.decode("utf-8"))
        if dockerId in stdout:
            return True
        return False

    # 获取一个可用的端口(自带并发锁)
    def getNewPort(self):
        # 获取端口，增加并发锁
        newPort = MysqlHandle().getMaxPort() + 1
        isUsed = True
        i = 0
        while (i < 5):
            if (self.portIsUsed(newPort) == True):
                newPort += 1
            else :
                isUsed = False
                break

        # 更新最新已使用的端口
        MysqlHandle().updateMaxPortConfig(newPort)

        # 提交事务，释放锁
        MysqlHandle().commit()

        # 端口已被使用,并超过重试次数，则退出
        if (isUsed == True):
            return False
        
        return newPort

    def portIsUsed(self, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect(('127.0.0.1', int(port)))
            return True
        except Exception:
            return False
