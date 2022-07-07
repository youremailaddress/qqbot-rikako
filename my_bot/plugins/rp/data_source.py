import os.path
from utils.dbhandler import SelfDefineDBHandler

class RPDBHandler(SelfDefineDBHandler):
    def __init__(self, path=os.path.split(os.path.realpath(__file__))[0]+"/rp.db"):
        super().__init__(path)
        self.cfg = [("USER_ID","INTEGER","PRIMARY KEY NOT NULL"),("RP","INTEGER","NOT NULL"),("COMMENT","TEXT","NOT NULL"),("UPDATETIME","TEXT","NOT NULL")]
        self.db,self.cursor = self.init()

    def init(self):
        db,cursor = self._ensureTable("deft",self.cfg)
        return db,cursor

    def push_rp(self,user_id,rp,comment,updatetime):
        self.cursor.execute("select count(*) from deft where USER_ID=? and UPDATETIME=?;",(user_id,updatetime))
        exists_ = self.cursor.fetchone()[0]
        if exists_ != 0:
            return False
        self.cursor.execute("insert or replace into deft (USER_ID,RP,COMMENT,UPDATETIME) values (?,?,?,?);",(user_id,rp,comment,updatetime))
        self.db.commit()
        return True

    def get_rp(self,user_id,updatetime):
        try:
            self.cursor.execute("select RP,COMMENT from deft where USER_ID=? and UPDATETIME=? limit 1;",(user_id,updatetime))
            rp,comment = self.cursor.fetchone()
            return (rp,comment)
        except Exception as e:
            print(str(e))
            return None