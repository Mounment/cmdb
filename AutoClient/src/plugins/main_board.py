#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__= 'luhj'
import os
import traceback
from .base import BasePlugin
from lib.response import BaseResponse

class MainBoardPlugin(BasePlugin):
    def linux(self):
        response = BaseResponse()
        try:
            if self.test_mode:
                from config import settings
                output = open(os.path.join(settings.BASEDIR,'files/board.out'),'r').read()
            else:
                shell_command = 'sudo dmidecode -t1'
                output = self.exec_shell_cmd(shell_command)

            response.data= self.parse(output)
        except Exception as e:
            msg = "%s linux mainboard plugin error:%s"
            self.logger.log(msg % (self.hostname, traceback.format_exc()), False)
            response.status = False
            response.error = msg % (self.hostname, traceback.format_exc())
        return response

    def parse(self,content):
        result = {}
        key_map ={
            'Manufacturer':'manufacturer',
            'Product Name':'model',
            'Serial Number':'sn'
        }
        for item in content.split('\n'):
            raw_data = item.strip().split(':')
            if len(raw_data) == 2:
                if raw_data[0] in key_map:
                    result[key_map[raw_data[0]]] = raw_data[1].strip()
        return result
