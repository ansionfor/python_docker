<p align="center">

  <h2 align="center">基于Flask Web + Docker的数据库资源申请项目</h3>
  <p align="center">
    通过restful api申请mysql、redis资源
    <br />
    <br>
  </p>

</p>

 
## 目录

- [上手指南](#上手指南)
  - [配置要求](#测试环境配置)
  - [Docker镜像](#docker镜像依赖)
  - [Python库依赖](#python库依赖)
- [安装步骤](#安装步骤)
- [流程图](#流程图)
- [文件目录说明](#文件目录说明)
- [项目特性](#项目特性)
- [接口文档](#接口文档)
  - [接口鉴权](#接口鉴权)
  - [创建mysql实例](#创建mysql实例)
  - [创建redis实例](#创建redis实例)
  - [获取实例列表](#获取用户的实例列表)
  - [获取实例详情](#获取用户单个实例详情)
- [TODO](#TODO)
- [作者](#作者)

## 上手指南


#### 测试环境配置

1. Centos 64位
2. Python 3.6
3. PIP 3
4. Docker 19.03.4
5. Mysql 5.7

#### Docker镜像依赖
1. Mysql 8.0
2. Redis 5.0

#### Python库依赖
1. Flask 2.0.1
2. Flask-RESTful 0.3.9
3. PyMySQL 0.9.3




## 安装步骤

1. 安装依赖库
```sh
# 安装python依赖
pip3 install -r requirements.txt

# 安装docker 镜像（mysql、redis）
docker pull mysql:8.0
docker pull redis:5.0
```
2. 克隆仓库

```sh
git clone https://github.com/ansionfor/python_docker.git
```

3、修改mysql配置(config/mysq.ini)
```
[mysql]
host=127.0.0.1
user=root
pwd=root
db=docker_demo
```

4、导入sql文件
```
source init.sql
```

5、启动
```
python3 main.py
```

<br>

## 流程图
![image](https://github.com/ansionfor/python_docker/blob/main/desc.png)

<br>

## 文件目录说明

```
├── api                                        # 接口目录
│   ├── Machine.py
│   ├── MysqlMachine.py
│   └── RedisMachine.py
├── common                                     # 公共库
│   ├── Auth.py                                # 鉴权类
│   ├── MysqlHandle.py                         # mysql操作类
├── config                                     # 配置目录 
│   └── mysql.ini
|── service                                    # 逻辑层
|    └── DockerSvr.py
├── init.sql                                   # 初始化sql
├── main.py                                    # 入口文件

```

## 项目特性
1. 自动生成端口、端口冲突检测
2. 自动生成账号密码
3. 并发安全创建实例
4. 代码分层，架构清晰

<br>

## 接口文档

<br>

#### 接口鉴权
<font size=2>每个请求需要在header带上Authorization信息，现有三个测试用户user1,user2,user3</font>

eg.
```
curl -X GET -H "Authorization:user1" 127.0.0.1:5000/list/1
```
<br>

#### 创建mysql实例

- Method: **POST**
- URL: ```/mysql```
- Headers： Content-Type:application/json
- Body:
```
{
    "charset":"utf8",
    "collection":"utf8_general_ci"
}
```

#### Response
- Body
```
{
    "code":200,
    "msg":"success",
    "data":{
        "host":"127.0.0.1",
        "user":"root",
        "pwd":56903401,
        "port":2001,
        "dockerId": "6aecdcdf980b"
    }
}
```
eg.

```
curl -X POST -H "Authorization:user1" -H "Content-Type:application/json" 127.0.0.1:5000/mysql -d '{"charset":"utf8"}'
```
<br>

#### 创建redis实例

- Method: **POST**
- URL: ```/redis```
- Headers： Content-Type:application/json
- Body:
```
{
    "memory":500     # 容器最大内存(M)
}
```

#### Response
- Body
```
{
    "code":200,
    "msg":"success",
    "data":{
        "host":"127.0.0.1",
        "pwd":56903401,
        "port":2002,
        "dockerId": "6aecdcdf980b"
    }
}
```
eg.

```
curl -X POST -H "Authorization:user1" -H "Content-Type:application/json" 127.0.0.1:5000/redis -d '{"memory":"400"}'
```
<br>

#### 获取用户的实例列表

- Method: **GET**
- URL: ```/list/<int:dockerType>```  # dockerType:mysql 1,redis 2
#### Response
- Body
```
{
    "code":200,
    "msg":"success",
    "data":[
        {
            "pwd":71880651,
            "host":"127.0.0.1",
            "port":2006,
            "user":"root",
            "dockerId":"6aecdcdf980b"
        }
    ]
}
```
eg.

```
curl -X GET -H "Authorization:user1" 127.0.0.1:5000/list/1
```
<br>

#### 获取用户单个实例详情

- Method: **GET**
- URL: ```/detail/<string:dockerId>```

#### Response
- Body
```
{
    "code":200,
    "msg":"success",
    "data":{
        "pwd":71880651,
        "host":"127.0.0.1",
        "port":2006,
        "user":"root",
        "dockerId":"6aecdcdf980b"
    }
}
```
eg.

```
curl -X GET -H "Authorization:user1" 127.0.0.1:5000/detail/6aecdcdf980b
```

## TODO
1. 容器内的数据跟配置映射到宿主机，容器内只存放运行环境
2. 使用gunicorn替换flask自带的wsgi，支持高并发
3. 增加supervisor管理常驻进程

## 作者
https://github.com/ansionfor




