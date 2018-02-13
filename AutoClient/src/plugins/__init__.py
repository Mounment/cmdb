
from src.plugins.basic import BasicPlugin
from config import settings
import importlib


def get_server_info(hostname=None):
    '''通过settings文件动态获取服务器的基本信息'''
    response = BasicPlugin(hostname).execute()
    if not response.status:
        return response

    for k,v in settings.PLUGINS_DICT.items():
        module_path,cls_name = v.rsplit('.',1)
        #动态去根据settings文件的字典找类
        cls = getattr(importlib.import_module(module_path),cls_name)
        obj = cls(hostname).execute()
        response.data[k] = obj
    return response


if __name__ == '__main__':
    ret = get_server_info()
    print(ret.__dict__)



