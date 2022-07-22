import os.path
from select import select
from utils.dbhandler import SelfDefineDBHandler

class BiliLiveDBHandler(SelfDefineDBHandler):
    def __init__(self, path=os.path.split(os.path.realpath(__file__))[0]+"/bililive.db"):
        super().__init__(path)
        self.cfg = [("USER","INTEGER","NOT NULL"),("GRP","INTEGER","NOT NULL"),("BILIID","INTEGER","NOT NULL"),("INGROUP","INTEGER","NOT NULL")]
        self.db,self.cursor = self.init()
    
    def init(self):
        db,cursor = self._ensureTable("deft",self.cfg)
        return db,cursor
    
    def push_blive(self,user,group,biliid):
        '''
        新增一个user的预约blive推送
        '''
        self.cursor.execute('select count(*) from deft where USER=? and GRP=? and BILIID=?;',(user,group,biliid))
        exists_ = self.cursor.fetchone()[0]
        if exists_ != 0:
            return False
        if self.count_blive(user) > 10:
            return False
        self.cursor.execute("insert or replace into deft (USER,GRP,BILIID,INGROUP) values (?,?,?,?);",(user,group,biliid,0))
        self.db.commit()
        return True

    def count_blive(self,user):
        '''
        查询一个user的预约blive推送个数
        '''
        self.cursor.execute("select count(*) from deft where USER=?;",(user,))
        exists_ = self.cursor.fetchone()[0]
        return exists_

    def show_in_group(self,user,group,biliid):
        self.cursor.execute('DELETE FROM deft where USER=? and GRP=? and BILIID=?;',(user,group,biliid))
        self.db.commit()
        self.cursor.execute("insert or replace into deft (USER,GRP,BILIID,INGROUP) values (?,?,?,?);",(user,group,biliid,1))
        self.db.commit()
        return True
        
    def remove_blive(self,user,biliid):
        self.cursor.execute('DELETE FROM deft where USER=? and BILIID=?;',(user,biliid))
        self.db.commit()
        return True
    
    def fetch_blive(self):
        retdic = {}
        self.cursor.execute("select distinct BILIID from deft;")
        lis = self.cursor.fetchall()
        for item in lis:
            retdic[item[0]] = []
            self.cursor.execute("select USER,GRP,INGROUP from deft where BILIID=?",(item[0],))
            slices = self.cursor.fetchall()
            for bar in slices:
                tempdic = {}
                tempdic['user'] = bar[0]
                tempdic['group'] = bar[1]
                tempdic['ingroup'] = bar[2]
                retdic[item[0]].append(tempdic)
        return retdic
    
    def freedbhandler(self):
        self.db.close()