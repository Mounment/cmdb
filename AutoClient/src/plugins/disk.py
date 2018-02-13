#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__= 'luhj'
import os
import traceback
from .base import BasePlugin
from lib import convert
import re
from lib.response import BaseResponse


class DiskPlugin(BasePlugin):
    def linux(self):
        response = BaseResponse()
        try:
            if self.test_mode:
                from config import settings
                output = open(os.path.join(settings.BASEDIR,'files/disk.out'),'r').read()
            else:
                shell_command = 'sudo MegaCli  -PDList -aALL'
                output = self.exec_shell_cmd(shell_command)
            response.data = self.parse(output)
        except Exception as e:
            msg = "%s linux disk plugin Error:%s"
            self.logger.log(msg % (self.hostname, traceback.format_exc()), False)
            response.status = False
            response.error = msg % (self.hostname, traceback.format_exc())
        return response

    def parse(self,content):
        response = {}
        result = []
        for row_line in content.split('\n\n\n\n'):
            result.append(row_line)
        for item in result:
            tmp_dic = {}
            for row in item.split('\n'):
                if not row.strip():continue
                if not len(row.split(':')) != 2:continue
                key,value = row.split(':')
                name= self.mega_patten_match(key)
                if name:
                    if key == 'Raw Size':
                        raw_size = re.search('(\d+\.\d+)',value.strip())
                        if raw_size:
                            tmp_dic[name] = raw_size.group()
                        else:
                            raw_size = '0'
                    else:
                        tmp_dic[name] = value.strip()
            if tmp_dic:
                response[tmp_dic['slot']] = tmp_dic

    @staticmethod
    def mega_patten_match(needle):
        grep_pattern = {'Slot': 'slot', 'Raw Size': 'capacity', 'Inquiry': 'model', 'PD Type': 'pd_type'}
        for key,value in grep_pattern.items():
            if needle.startswith(needle):
                return value

        return False





