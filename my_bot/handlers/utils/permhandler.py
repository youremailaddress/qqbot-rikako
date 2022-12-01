from utils.core.db.permdb import PermissionDB
from utils.core.tools.user import Unit

class PermissionHandler(PermissionDB):
    def __init__(self) -> None:
        super().__init__()
    
    def check_Unit(self,uid:str,gid:str):
        '''
        判断uid/gid组合是否合逻辑
        '''
        try:
            m = Unit(uid,gid)
        except:
            return False
        return True
    
    def get_Func_Perm(self,funcname:str,isblack=False):
        '''
        获取某函数的Perm相关的Unit列表
        '''
        a = self.select_perms_by_func(funcname,isblack)
        a = [Unit(i[1],i[2]) for i in a]
        return a
    