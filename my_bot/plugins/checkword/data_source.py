from utils.dbhandler import DbHandler
from .model import CheckWord,CheckWordBase
from utils.functions import getDir
import time
class CheckWordDBHandler(DbHandler):
    def __init__(self, path=getDir("databases/checkword.db"), Base=CheckWordBase):
        super().__init__(path, Base)
        self.staletime = 5000*60
    
    def check_checkword(self,uid,checkwd):
        # 检查并勾销使用状态，返回 True（通过）和 False（否决），同时修改对应列 isused
        if not self.session.query(CheckWord).filter(CheckWord.user==uid,CheckWord.isused=="0",CheckWord.check==checkwd,int(time.time())-CheckWord.updatetime<self.staletime).count():
            return False
        else:
            cw = self.session.query(CheckWord).filter(CheckWord.user==uid,CheckWord.isused==False,CheckWord.check==checkwd,int(time.time())-CheckWord.updatetime<self.staletime).one()
            self.session.merge(CheckWord(user=cw.user,check=cw.check,isused="1",updatetime=cw.updatetime))
            self.session.commit()
            return True

    def push_checkword(self,uid,checkwd):
        # 添加 checkword
        self.session.add(CheckWord(user=uid,check=checkwd,updatetime=str(int(time.time())),isused="0"))
        self.session.commit()
        return True
        

CWDBH = CheckWordDBHandler()