



class BaseResponse(object):
    '''请求体'''
    def __init__(self):
        self.status = True
        self.message = None
        self.data = None
        self.error = None
