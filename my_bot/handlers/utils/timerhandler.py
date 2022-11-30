from utils.core.db.timerdb import TimerDB
from utils.core.tools.user import User

class TimerHandler(TimerDB):
    def __init__(self) -> None:
        super().__init__()
    
    def check_Expand(self,uid:str):
        try:
            m = User(uid)
            return m.isexpand
        except:
            return None
    
    def get_user_by_id(self,id:int):
        a = self.select_timer_by_id(id)
        if a == None:
            return None
        else:
            return a[2]