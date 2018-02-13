

from lib.log import Logger
from config import settings

class BasePlugin(object):

    def __init__(self,hostname=''):
        '''根据setting文件的mode执行对应的方法'''
        self.logger = Logger()
        self.test_mode = settings.TEST_MODE
        self.mode_list = ['agent','ssh','salt']
        if hasattr(settings,'MODE'):
            self.mode = settings.MODE
        else:
            self.mode = 'agent'
        self.hostname = hostname


    def salt(self,cmd):
        '''saltstack执行远程命令'''
        import salt.client

        local = salt.client.LocalClient()
        result = local.cmd(self.hostname,'cmd.run',[cmd])
        return result[self.hostname]


    def ssh(self,cmd):
        '''ssh执行远程命令'''
        import paramiko
        private_key = paramiko.RSAKey.from_private_key(settings.SSH_PRIVATE_KEY)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.hostname,port=settings.SSH_PORT,username=settings.SSH_USER,pkey=private_key)
        stdin,stdout,stderr = ssh.exec_command(cmd)
        res = stdout.read()
        ssh.close()
        return res

    def agent(self,cmd):
        import subprocess

        output = subprocess.getoutput(cmd)
        return output

    def exec_shell_cmd(self,cmd):
        '''根据mode找到相应的方法执行命令'''
        if self.mode not in self.mode_list:
            raise Esxception("settings.mode must be one of ['agent', 'salt', 'ssh']")
        func = getattr(self,self.mode)
        output = func(cmd)
        return output

    def execute(self):
        return self.linux()

    def linux(self):
        raise Exception('You must implement linux method.')











