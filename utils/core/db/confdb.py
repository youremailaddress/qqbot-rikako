from utils.core.db import *

class ConfigDB(FuncDB):
    def __init__(self) -> None:
        super().__init__()

    def add_conf(self,fid:int,uid:str,params:str):
        '''
        add_conf:添加conf
        fid:验证过的funcid
        uid:未扩展的userid
        params:个性化参数
        '''
        try:
            self.session.add(Personalize(fid=fid,uid=uid,params=params,isdefault = "0"))
            self.session.commit()
            return True
        except:
            self.session.rollback()
            return False

    def set_main_conf(self,id:int):
        '''
        set_main_conf:设为默认设置
        '''
        try:
            self.session.query(Personalize).filter(Personalize.id==id).update({'isdefault': "1"})
            self.session.commit()
            return True
        except:
            self.session.rollback()
            return False

    def unset_main_conf(self,id:int):
        '''
        unset_main_conf:取消默认设置
        '''
        try:
            self.session.query(Personalize).filter(Personalize.id==id).update({'isdefault': "0"})
            self.session.commit()
            return True
        except:
            self.session.rollback()
            return False

    def has_main_conf(self,fid:int,uid:str):
        '''
        has_main_conf:某人某函数是否存在默认设置
        '''
        return True if self.session.query(Personalize).filter(Personalize.fid==fid,Personalize.uid==uid,Personalize.isdefault=="1").count() > 0 else False

    def get_main_conf(self,fid:int,uid:str):
        '''
        get_main_conf:获取某人某函数的默认设置
        '''
        if not self.has_main_conf(fid,uid):
            return None
        else:
            a = self.session.query(Personalize).filter(Personalize.fid==fid,Personalize.uid==uid,Personalize.isdefault=="1").one()
            return (a.id,a.fid,a.func.name,a.uid,a.params,a.isdefault)

    def get_user_conf(self,uid:str):
        '''
        get_user_conf:获取某人的设置
        '''
        res = self.session.query(Personalize).filter(Personalize.uid==uid).all()
        return [(i.id,i.fid,i.func.name,i.uid,i.params,i.isdefault) for i in res]

    def get_user_func_conf(self,fid:int,uid:str):
        '''
        get_user_func_conf:获取某人对某函数的设置
        '''
        res = self.session.query(Personalize).filter(Personalize.uid==uid,Personalize.fid==fid).all()
        return [(i.id,i.fid,i.func.name,i.uid,i.params,i.isdefault) for i in res]

    def del_conf(self,id:int):
        '''
        del_conf:根据id删除某config
        '''
        try:
            self.session.query(Personalize).filter(Personalize.id==id).delete()
            self.session.commit()
            return True
        except:
            self.session.rollback()
            return False
