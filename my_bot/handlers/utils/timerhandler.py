from utils.core.db.timerdb import TimerDB
from utils.core.tools.user import User

class TimerHandler(TimerDB):
    def __init__(self) -> None:
        super().__init__()
    
    def check_Expand(self,uid:str):
        '''
        判断一个uid是否是expand过的
        '''
        try:
            m = User(uid)
            return m.isexpand
        except:
            return None
    
    def get_user_by_id(self,id:int):
        '''
        根据 timerid 找到 user
        '''
        a = self.select_timer_by_id(id)
        if a == None:
            return None
        else:
            return a[2]
        
    def get_timer_by_name(self,name:str):
        '''
        根据函数名称返回元组列表，元组结构为(uid,gid,start,interval,pid)
        '''
        a = self.select_timer_by_name(name)
        return [(i[2],i[3],i[4],i[5],i[6]) for i in a]
