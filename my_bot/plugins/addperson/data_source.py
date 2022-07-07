import os
from utils.dbhandler import SelfDefineDBHandler

class FriendsDB(SelfDefineDBHandler):
    def __init__(self, num=5,path=os.path.split(os.path.realpath(__file__))[0]+"/friends.db"):
        super().__init__(path)
        self.cfg = [("USER_ID","INTEGER","PRIMARY KEY NOT NULL"),("UPDATETIME","TEXT","NOT NULL")]
        self.db,self.cursor = self.init()
        self.num = num

    def init(self):
        db,cursor = self._ensureTable("deft",self.cfg)
        return db,cursor

    def checknum(self,time):
        '''
        True: 可以添加
        False：不能添加
        '''
        self.cursor.execute("select count(*) from deft where UPDATETIME=?;",(time,))
        res = self.cursor.fetchone()[0]
        if res <= self.num:
            return True
        else:
            return False

    def push_person(self,user_id,time):
        try:
            self.cursor.execute("insert or replace into deft (USER_ID,UPDATETIME) values (?,?);",(user_id,time))
            self.db.commit()
        except:
            self.db.rollback()