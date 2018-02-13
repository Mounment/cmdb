
from .response import BaseResponse
from json.encoder import JSONEncoder
import json as default_json


class JsonEncoder(JSONEncoder):
    #将response对象转换为json格式
    def default(self, o):
        if isinstance(o,BaseResponse):
            return o.__dict__
        return JSONEncoder.default(self,o)


class Json(object):
    @staticmethod
    def dumps(response,ensure_ascii=True):
        return default_json.dumps(response,ensure_ascii=ensure_ascii,cls=JsonEncoder)


