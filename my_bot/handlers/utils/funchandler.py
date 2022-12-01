from utils.core.db.funcdb import FunctionDB

class FunctionHandler(FunctionDB):
    def __init__(self) -> None:
        super().__init__()
    
    def register(self,name:str,intro:str,usage:str,istimer:bool,paramstring:str):
        '''
        注册函数 返回 True 或者 False
        '''
        return self.add_func(name,intro,usage,istimer,paramstring)

    def getFuncid(self,name:str):
        '''
        根据函数名获取函数id 如果不存在则返回 False
        '''
        return self.get_id_by_name(name)
    
    def isTimerFunc(self,name:str):
        '''
        根据函数名确定是否为定时任务函数
        '''
        fid = self.getFuncid(name)
        if fid == False:
            return False
        return self.select_func_by_id(fid)[3]

    def getParamstring(self,fid:int):
        try:
            return self.select_func_by_id(fid)[4]
        except:
            return None