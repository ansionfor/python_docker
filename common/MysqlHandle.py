import configparser,os,pymysql,time


class MysqlHandle():
    def __init__(self):
        configPath = os.getcwd() + '/config/mysql.ini'
        config = configparser.ConfigParser()
        config.read(configPath, encoding='utf-8')
        mysql = config['mysql']
        self.db = pymysql.connect(mysql['host'], mysql['user'],mysql['pwd'], mysql['db'], cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.db.cursor()
        self.table = 'user_docker_list'
        self.configTable = 'config'
        self.defaultPort = 2000
    
    # 提交事务
    def commit(self):
        res = self.db.commit()
        self.cursor.close()
        self.db.close()
        return res

    # 新增实例
    def insertDocker(self, userId, dockerId, dockerType=1, dbInfo='', port = -1):
        sql = "insert into " + self.table + " values (null, %s, %s, %s, %s, %s, %s, %s, %s)"
        nowTime = time.time()
        try:
            self.cursor.execute(sql, (userId, dockerId, dockerType, dbInfo, port, nowTime, 0, 0))
            self.commit()
            return True
        except Exception:
            print("Error: unable to insert data")
            return False
    
    # 获取用户的所有实例
    def getAllDockersByUserId(self, userId, dockerType):
        sql = "select * from " + self.table + " where user_id=%s and docker_type=%s and deleted=0"
        res = []
        try:
            self.cursor.execute(sql, (userId, dockerType))
            res = self.cursor.fetchall()
        except Exception:
            print ("Error: unable to fetch data")
        self.commit()
        return res

    # 获取一台实例信息
    def getOneDockerByUserIdAndDockerId(self, userId, dockerId):
        sql = "select * from " + self.table + " where user_id = %s and docker_id = %s"
        cur = self.cursor
        res = []
        try:
            cur.execute(sql, (userId, dockerId))
            res = cur.fetchone()
        except:
            print ("Error: unable to fetch data")
        self.commit()
        return res
    
    # 获取当前已使用的最大端口号（并发安全）
    def getMaxPort(self):
        sql = "select intval as port from " + self.configTable + " where name='max_used_port' limit 1 for update"
        cursor = self.cursor
        result = []
        try:
            cursor.execute(sql)
            result = cursor.fetchone()
        except Exception:
            print ("Error: unable to fetch data")
        return self.defaultPort if len(result) == 0 else result['port']



    def updateMaxPortConfig(self, port):
        sql = "update " + self.configTable + " set intval = %s where name = 'max_used_port'" 
        cur = self.cursor
        try:
            cur.execute(sql, port)
            self.commit()
            return True
        except Exception:
            print("Error: unable to update max port")
            return False
        
