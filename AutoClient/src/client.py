
import hashlib
import os
import time
import requests
import json
from config import settings
from lib.log import Logger
from lib.serialize import Json
from src import plugins
from concurrent.futures import ThreadPoolExecutor

class AutoBase(object):
    def __init__(self):
        self.asset_api = settings.ASSET_API
        self.key = settings.KEY
        self.key_name = settings.AUTH_KEY_NAME

    def auth_key(self):
        '''接口认证'''
        ha = hashlib.md5(self.key.encode('utf8'))
        time_span = time.time()
        ha.update(bytes('%s|%f' %(self.key,time_span),encoding='utf8'))
        encryption = ha.hexdigest()
        result = '%s|%f'%(encryption,time_span)
        return {self.key_name:result}

    def get_asset(self):
        '''get方式获取未采集的资产'''
        try:
            headers = {}
            headers.update(self.auth_key())
            response = requests.get(
                url=self.asset_api,
                headers=headers
            )
        except Exception as e:
            response = e
        return response.json()


    def post_asset(self,msg,callback=None):
        '''以post方式提交信息'''
        status = True
        try:
            headers = {}
            headers.update(self.auth_key())
            response = requests.post(
                url=self.asset_api,
                headers=headers,
                json=msg
            )
        except Exception as e:
            response = e
            status = False
        if callback:
            callback(status,response)

    def process(self):
        '''继承此方法作为处理请求的入口'''
        raise NotImplementedError('you must implement process method')

    def callback(self,status,response):
        '''提交资产后的回调函数'''
        if not status:
            Logger().log(str(response),False)
            return
        ret = json.loads(response.text)
        if ret['code'] == 1000:
            Logger().log(ret['message'],True)
        else:
            Logger().log(ret['message'], False)


class AutoAgent(AutoBase):
    def __init__(self):
        self.cert_file_path = settings.CERT_FILE_PATH
        super(AutoAgent,self).__init__()

    def load_local_cert(self):
        '''读本地的主机文件'''
        if not os.path.exists(self.cert_file_path):
            return None
        with open(self.cert_file_path,'r') as f:
            data = f.read()
        if not data:
            return None
        cert = data.strip()
        return cert


    def write_local_cert(self,cert):
        '''写本地的主机文件'''
        if not os.path.exists(self.cert_file_path):
            os.makedirs(os.path.basename(self.cert_file_path))
        with open(settings.CERT_FILE_PATH,'w') as f:
            f.write(cert)


    def process(self):
        '''
        获取当前资产的信息
        1,在资产中获取主机名 cert_new
        2,在本地cert文件中获取主机名 cert_old
        :return:
        '''
        server_info = plugins.get_server_info()
        if not server_info.status:
            return
        local_sert = self.load_local_cert()
        if local_sert:
            if local_sert == server_info.data['hostname']:
                pass
            else:
                server_info.data['hostname'] = local_sert
        else:
            self.write_local_cert(server_info.data['hostname'])
        server_json = Json.dumps(server_info.data)
        self.post_asset(server_json,self.callback)

class AutoSSH(AutoBase):

    def process(self):
        '''
        根据主机名获取资产信息,发送给api
        :return:
        '''
        task = self.get_asset()
        if not task['status']:
            Logger().log(task['message'],False)
        #使用线程池实现
        pool = ThreadPoolExecutor(10)
        for item in task['data']:
            hostname = item['hostname']
            pool.submit(self.run,hostname)
        pool.shutdown(wait=True)


    def run(self):
        server_info = plugins.get_server_info()
        server_json = Json.dumps(server_info.data)
        self.post_asset(server_json,self.callback)


class AutoSalt(AutoBase):
    def process(self):
        task = self.get_asset()
        if not task['status']:
            Logger().log(task['message'],False)

        pool = ThreadPoolExecutor(10)
        for item in task['data']:
            hostname = item['hostname']
            pool.submit(self.run,hostname)
        pool.shutdown(wait=True)

    def run(self):
        server_info = plugins.get_server_info()
        server_json = Json.dumps(server_info.data)
        self.post_asset(server_json,self.callback)








