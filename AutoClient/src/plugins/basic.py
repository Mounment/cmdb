
import traceback
from .base import BasePlugin
from lib.response import BaseResponse


class BasicPlugin(BasePlugin):

    def os_platform(self):
        '''获取操作系统类型'''
        if self.test_mode:
            output = 'linux'
        else:
            output = self.exec_shell_cmd('hostname')
        return output.strip()


    def os_version(self):
        '''获取操作系统版本'''
        if self.test_mode:
            output = 'CentOS release 6.6 (Final)\nKernel \r on an \m'
        else:
            output = self.exec_shell_cmd('cat /etc/issue')
        return output.strip().split('\n')[0]


    def os_hostname(self):
        '''获取主机名'''
        if self.test_mode:
            output = 'c1.com'
        else:
            output = self.exec_shell_cmd('hostname')
        return output.strip()

    def linux(self):
        response = BaseResponse()
        try:
            ret = {
                'os_platform':self.os_platform(),
                'os_version':self.os_version(),
                'os_hostname':self.os_hostname()
            }
            response.data = ret
        except Exception as e:
            msg = "%s BasicPlugin Error:%s"
            self.logger.log(msg % (self.hostname,traceback.format_exc()),False )
            response.status = False
            response.error = msg % (self.hostname,traceback.format_exc())
        return response
