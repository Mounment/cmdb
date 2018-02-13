import os
import traceback
from .base import BasePlugin
from lib import convert
from lib.response import BaseResponse


class MemoryPlugin(BasePlugin):

    def linux(self):
        response = BaseResponse()
        try:
            if self.mode:
                from config import settings
                output = open(os.path.join(settings.BASEDIR,'files/memory.out'),'r').read()
            else:
                shell_command = 'sudo dmidecode  -q -t 17 2>/dev/null'
                output=self.exec_shell_cmd(shell_command)
            response = self.parse(output)
        except Exception as e:
            msg = "%s linux memory plugin error:%s"
            self.logger.log(msg % (self.hostname, traceback.format_exc()), False)
            response.status = False
            response.error = msg % (self.hostname, traceback.format_exc())
        return response


    def parse(self,content):
        ram_dic = {}
        key_map = {
            'Size':'capacity',
            'Locator':'slot',
            'Type':'model',
            'Speed':'speed',
            'Manufacturer':'manufacturer',
            'Serial Number':'sn'
        }
        devices = content.split('Memory Device')
        for item in devices:
            item = item.strip()
            if not item:
                continue
            if item.startswith('#'):
                continue
            segment = {}
            lines = item.split('\n\t')
            for line in lines:
                if len(line.split(':')) > 1:
                    key,value = line.split(':')
                else:
                    key = line.split(':')[0]
                    value = ''
                if key in key_map:
                    if key == 'Size':
                        segment[key_map['Size']] = convert.convert_mb_to_gb(value,0)
                    else:
                        segment[key_map[key.strip()]] = value.strip()
            ram_dic[segment['slot']] = segment

        return ram_dic
