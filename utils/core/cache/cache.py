import json
from utils.path.pathparser import getDir,pathExists

class CacheHandler():
    # 一个缓存机制 目的是方便 web 端进行鉴权
    # 里面存储了（最多一天内的）好友和群聊以及群聊中的人、角色对应关系
    def __init__(self,path=getDir("databases/friends.json")):
        self.path = path
        self.friend = {}
        self.group = {}
        self.frigro = {}
        if not pathExists(self.path):
            self.exportdata()
        else:
            self.importdata()

    def importdata(self):
        # 从硬盘读取数据
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
        # 把数据存回硬盘
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
        # 更新时对新的 friendslis 进行处理 由于存在 admin 的 remark 所以不能简单覆盖
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
        # 更新时对新的 grouplis 进行处理 不能覆盖原因同上
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
        # 更新群聊里成员 直接覆盖
        tempdic = {}
        for k,v in frigrodic.item():
            grp = k
            for i in v:
                tempdic[(grp,i["user_id"])] = i['role']
        self.frigro = tempdic

    def get_uid_and_remark(self):
        # 获取好友和 remark
        return self.friend

    def get_gid_and_remark(self):
        # 获取群聊和 remark
        return self.group

    def get_gid_and_type(self,uid):
        # 给定具体的uid，获取所在的群聊和扮演的群内角色列表
        retlis = []
        for gid in self._get_all_gid():
            if self.frigro.get((gid,uid)) != None:
                retlis.append((gid,self.frigro[(gid,uid)]))
        return retlis

    def change_remark_friend(self,uid,remark):
        # 修改某个好友的 remark
        if self.friend.get(uid) != None:
            self.friend[uid] = remark
            return True
        else:
            return False

    def change_remark_group(self,gid,remark):
        # 修改某个群组的remark
        if self.group.get(gid) != None:
            self.group[gid] = remark
            return True
        else:
            return False