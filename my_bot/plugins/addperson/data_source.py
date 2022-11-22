from utils.dbhandler import DbHandler
from .model import FRI,FriendBase
from utils.functions import getDir
class FRIDBHandler(DbHandler):
    def __init__(self, path=getDir("databases/friends.db"), Base=FriendBase):
        super().__init__(path, Base)
    
    def checknum(self,time):
        '''
        True: 可以添加
        False：不能添加
        '''
        if self.session.query(FRI).filter(FRI.updatetime==time).count() > 5:
            return False
        else:
            return True
    
    def push_person(self,userid,time):
        self.session.merge(FRI(id=userid,updatetime=time))
        self.session.commit()
    
FRDBH = FRIDBHandler()