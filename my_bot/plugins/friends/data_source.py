from utils.dbhandler import DbHandler
from .model import FRI,FriendBase
from utils.functions import getDir
from os.path import exists
import json
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

class FRIHandler():
    def __init__(self,path=getDir("databases/friends.json")):
        self.path = path
        self.friend = {}
        self.group = {}
        self.frigro = {}
        if not exists(self.path):
            self.exportdata()
        else:
            self.importdata()

    def importdata(self):
        dic = {}
        with open(self.path,"r",encoding="UTF8") as f:
            dic = json.loads(f.read())
        self.friend = dic["friend"]
        self.group = dic["group"]
        temp = dic["frigro"]
        self.frigro = {}
        for k,v in temp.items():
            self.frigro[eval(k)] = v

    def exportdata(self):
        dic = {}
        tempdic = {}
        for k,v in self.frigro.items():
            tempdic[str(k)] = v
        dic["friend"] = self.friend
        dic["group"] = self.group
        dic["frigro"] = tempdic
        with open(self.path,"w",encoding="UTF8") as f:
            f.write(json.dumps(dic,ensure_ascii=False))
    
    def _get_all_uid(self):
        # friend表 获取所有 uid list
        return list(self.friend.keys())

    def _get_all_gid(self):
        # group表 获取所有 gid list
        return list(self.group.keys())

    def handle_data_friends(self,friendslis):
        m = {}
        for item in friendslis:
            m[item['user_id']] = item['remark']
        updateduid = set(m.keys())
        olduid = set(self._get_all_uid())
        add = updateduid - olduid
        delete = olduid - updateduid
        for uid in add:
            self.friend[uid] = m[uid]
        for uid in delete:
            del self.friend[uid]

    def handle_data_group(self,grouplis):
        m = {}
        for item in grouplis:
            m[item["group_id"]] = item["group_name"]
        updatedgid = set(m.keys())
        oldgid = set(self._get_all_gid())
        add = updatedgid - oldgid
        delete = oldgid - updatedgid
        for gid in add:
            self.group[gid] = m[gid]
        for gid in delete:
            del self.group[gid]

    def handle_data_frigro(self,frigrodic):
        tempdic = {}
        for k,v in frigrodic.item():
            grp = k
            for i in v:
                tempdic[(grp,i["user_id"])] = i['role']
        self.frigro = tempdic

    def get_uid_and_remark(self):
        return self.friend

    def get_gid_and_remark(self):
        return self.group

    def get_gid_and_type(self,uid):
        retlis = []
        for gid in self._get_all_gid():
            if self.frigro.get((gid,uid)) != None:
                retlis.append((gid,self.frigro[(gid,uid)]))
        return retlis

    def change_remark_friend(self,uid,remark):
        if self.friend.get(uid) != None:
            self.friend[uid] = remark
            return True
        else:
            return False

    def change_remark_group(self,gid,remark):
        if self.group.get(gid) != None:
            self.group[gid] = remark
            return True
        else:
            return False
    
FRDBH = FRIDBHandler()
FRIH = FRIHandler()