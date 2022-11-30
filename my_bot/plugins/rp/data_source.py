from utils.db.dbhandler import DbHandler
from .model import RP,RPBase
from utils.functions import getDir
class RPDBHandler(DbHandler):
    def __init__(self, path=getDir("databases/rp.db"), Base=RPBase):
        super().__init__(path, Base)
    
    def push_rp(self,user_id,rp,comment,updatetime):
        if self.session.query(RP).filter(RP.id==user_id,RP.updatetime==updatetime).count():
            return False
        self.session.merge(RP(id=user_id,rp=rp,comment=comment,updatetime=updatetime))
        self.session.commit()
        return True

    def get_rp(self,user_id,updatetime):
        try:
            rpins =self.session.query(RP).filter(RP.id==user_id,RP.updatetime==updatetime).one()
        except:
            return None
        return rpins.rp,rpins.comment

RPH = RPDBHandler()