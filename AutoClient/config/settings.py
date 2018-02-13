import os

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


#用于API认证的key
KEY = '299095cc-1330-11e5-b06a-a45e60bec08b'

#用于API认证的请求头
AUTH_KEY_NAME = 'auth-key'

#错误日志
ERROR_LOG_FILE = os.path.join(BASEDIR,'log','error.log')

#运行日志
RUN_LOG_FILE = os.path.join(BASEDIR,'log','run.log')

#Agent模式保存服务器唯一的主机ID
CERT_FILE_PATH = os.path.join(BASEDIR,'config','cert')

#是否启用测试模式(从文件中获取数据)
TEST_MODE = True

#采集资产的方式(ssh,salt,agent)
MODE = 'ssh'

#如果是ssh方式,要配置key和user
SSH_PRIVATE_KEY = '/home/auto/.ssh/id_rsa'
SSH_USER = 'root'
SSH_PORT = 22

#采集硬件数据的插件
PLUGINS_DICT = {
    'cpu': 'src.plugins.cpu.CpuPlugin',
    'disk': 'src.plugins.disk.DiskPlugin',
    'main_board': 'src.plugins.main_board.MainBoardPlugin',
    'memory': 'src.plugins.memory.MemoryPlugin',
    'nic': 'src.plugins.nic.NicPlugin',
}

#资产信息API
ASSET_API = 'http://127.0.0.1:8000/api/asset'