import json

class Jsonify():
    def __init__(self,jsonstring:str) -> None:
        self.js = self.LoadJson(jsonstring)
        assert self.js != None
        
    def getRequired(self):
        '''
        从 func 的设置字段获取必填项 
        '''
        req = set()
        for k,v in self.js.items():
            if v == 1:
                req.add(k)
        return req

    def getOptional(self):
        '''
        从 func 的设置字段获取选填项
        '''
        _all = set(self.js.keys())
        req = self.getRequired()
        return _all - req

    def LoadJson(self,jsonstring:str):
        '''
        加载 jsonstring
        '''
        try:
            return json.loads(jsonstring)
        except:
            return None
    
    def preParamProcess(self,paramstring:str):
        '''
        把用户设置里和函数规定传入参数相同的部分以dic形式返回 如果未填必填项 则返回 None
        '''
        m = self.LoadJson(paramstring)
        if m == None:
            return None
        retdic = {}
        req = self.getRequired()
        if req - set(m.keys()) != set():
            return None
        for k,v in m.items():
            if k in self.js.keys():
                retdic[k] = v
        return retdic
    
    @staticmethod
    def wrapReqOpt(req:list,opt:list):
        ret = {}
        for item in req:
            ret[item] = 1
        for item in opt:
            ret[item] = 0
        return json.dumps(ret)

        