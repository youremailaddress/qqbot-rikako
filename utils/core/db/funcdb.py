from utils.core.db import *

class FunctionDB(FuncDB):
    def __init__(self) -> None:
        super().__init__()
    
    def add_func(self,name:str,intro:str,usage:str,istimer:bool=False,paramstring:str="{}") -> bool:
        '''
        name:函数名 不可重复
        intro:函数介绍
        usage:函数用法
        istimer:bool 是否为定时函数
        paramstring:json dumps 参数列表 1为required 0为optional
        '''
        if self.get_id_by_name(name) != False:
            try:
                self.session.merge(Func(id=self.get_id_by_name(name),name=name,intro=intro,usage=usage,istimer="1" if istimer==True else "0",paramstring=paramstring))
                self.session.commit()
                return True
            except:
                self.session.rollback()
                return False
        else:
            try:
                self.session.add(Func(name=name,intro=intro,usage=usage,istimer="1" if istimer==True else "0",paramstring=paramstring))
                self.session.commit()
                return True
            except:
                self.session.rollback()
                return False

    def select_func_by_name(self,name:str) -> tuple:
        '''
        name:函数名
        select_func_by_name:根据函数名查找其他值,返回元组（介绍，用法，是否定时[bool],paramstring）或None
        '''
        try:
            res = self.session.query(Func).filter(Func.name==name).one()
            return (res.id,res.intro,res.usage,True if res.istimer == "1" else False,res.paramstring)
        except:
            self.session.rollback()
            return None
    
    def select_func_by_id(self,id:int) -> tuple:
        try:
            res = self.session.query(Func).filter(Func.id==id).one()
            return (res.name,res.intro,res.usage,True if res.istimer == "1" else False,res.paramstring)
        except:
            self.session.rollback()
            return None
    
    def get_name_by_id(self,id:int):
        res = self.select_func_by_id(id)
        if res == None:
            return False
        else:
            return res[0]
    
    def get_id_by_name(self,name:str):
        res = self.select_func_by_name(name)
        if res == None:
            return False
        else:
            return res[0]

    def get_all_func(self):
        res = self.session.query(Func).all()
        return [(i.name,i.intro,i.usage) for i in res]