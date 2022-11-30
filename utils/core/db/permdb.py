from utils.core.db import *

class PermissionDB(FuncDB):
    def __init__(self) -> None:
        super().__init__()

    def add_perm(self,fid:int,uid:str,gid:str,isblack:bool=False) -> bool:
        '''
        fid:已经检查过的存在的 funcid
        uid:已经检查过的合法的扩展uid
        gid:已经检查过的合法的扩展gid
        isblack:写入的是否是黑名单表
        add_perm:插入perm相关数据库
        '''
        if isblack:
            M = Disable
        else:
            M = Func_User
        try:
            self.session.add(M(fid=fid,uid=uid,gid=gid))
            self.session.commit()
            return True
        except:
            self.session.rollback()
            return False

    def del_perm(self,fid:int,uid:str,gid:str,isblack:bool=False) -> bool:
        '''
        fid:已经检查过的存在的 funcid
        uid:已经检查过的合法的扩展uid
        gid:已经检查过的合法的扩展gid
        isblack:是否是黑名单表
        del_perm:删除perm相关数据库数据
        '''
        if isblack:
            M = Disable
        else:
            M = Func_User
        try:
            self.session.query(M).filter(M.fid==fid,M.uid==uid,M.gid==gid).delete()
            self.session.commit()
            return True
        except:
            self.session.rollback()
            return False
        
    def select_all_perms(self,isblack:bool=False) -> list:
        '''
        isblack:是否是黑名单表
        select_perms:查询perm相关整表
        '''
        if isblack:
            M = Disable
        else:
            M = Func_User
        try:
            return [(item.fid,item.uid,item.gid) for item in self.session.query(M).all()]
        except:
            self.session.rollback()
            return []
    
    def select_perms_by_func(self,name:str,isblack:bool=False) -> list:
        if isblack:
            M = Disable
        else:
            M = Func_User
        try:
            return [(item.fid,item.uid,item.gid) for item in self.session.query(M).join(Func).filter(Func.name == name).all()]
        except:
            self.session.rollback()
            return []