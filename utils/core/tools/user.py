class Expand():
    def __init__(self) -> None:
        self.isexpand = False
        self.ischecked = False

class Unit(Expand):
    def __init__(self,uid:str,gid:str) -> None:
        super().__init__()
        self.uid = User(uid)
        self.gid = Group(gid)
        self.is_checked()
        assert self.is_checked
        
    def is_checked(self):
        if not self.uid.uid.isdigit() and self.uid.uid not in ["*","#1","#2","#3","#4"]:
            self.ischecked = False
        if self.gid.gid=="@" and self.uid.uid in ["#1","#2","#3","#4"]:
            self.ischecked = False
        if not self.gid.gid.isdigit() and self.gid.gid not in ["*","@"]:
            self.ischecked = False
        self.ischecked = True

    def __contains__(self,item):
        # item tuple : uid,gid,role 都是 str 类型
        if isinstance(item,tuple) == False or len(item) != 3:
            return False
        uid,gid,role = item
        if self.gid.gid == '*':# 任意群聊
            if gid == None: # 私聊
                return False
            if (self.uid.uid == '*'):# 如果是任意人,恒真
                return True
            elif (self.uid.uid == '#1'):  # 如果是任意群主
                if role == 'owner':
                    return True
                else:
                    return False
            elif (self.uid.uid == '#2'): # 如果是任意管理
                if role == 'admin':
                    return True
                else:
                    return False
            elif (self.uid.uid == '#3'): # 如果是任意成员
                if role == 'member':
                    return True
                else:
                    return False
            elif (self.uid.uid == '#4'): # 如果是任意匿名用户
                if role == None and uid == '80000000':
                    return True
                else:
                    return False
            else:                # 如果是任意群聊指定人
                if uid == self.uid.uid:
                    return True
                else:
                    return False
        elif (self.gid.gid == '@'): # 私聊
            if gid != None: # 群聊
                return False
            if (self.uid.uid == '*'): # 如果是任意人,恒真
                return True
            else:
                if uid == self.uid.uid:
                    return True
                else:
                    return False
        else:
            if gid != self.gid.gid:
                return False
            if (self.uid.uid == '*'): # 如果是任意人,恒真
                return True
            elif (self.uid.uid == '#1'):  # 如果是群主
                if role == 'owner':
                    return True
                else:
                    return False
            elif (self.uid.uid == '#2'): # 如果是管理
                if role == 'admin':
                    return True
                else:
                    return False
            elif (self.uid.uid == '#3'): # 如果是成员
                if role == 'member':
                    return True
                else:
                    return False
            elif (self.uid.uid == '#4'): # 如果是匿名用户
                if role == None and uid == '80000000':
                    return True
                else:
                    return False
            else:                # 如果是群聊指定人
                if uid == self.uid.uid:
                    return True
                else:
                    return False
        

class User(Expand):
    def __init__(self,uid:str) -> None:
        super().__init__()
        self.uid = self.check_is_expand(uid)
        assert self.ischecked

    def check_is_expand(self,uid:str):
        if uid.isdigit():
            self.isexpand = False
            self.ischecked = True
        elif uid in ["*","#1","#2","#3","#4"]:
            self.isexpand = True
            self.ischecked = True
        else:
            self.ischecked = False
            self.isexpand = False
        return uid

class Group(Expand):
    def __init__(self,gid:str) -> None:
        super().__init__()
        self.gid = self.check_is_expand(gid)
        assert self.ischecked

    def check_is_expand(self,gid:str):
        if gid.isdigit():
            self.isexpand = False
            self.ischecked = True
        elif gid in ["*","@"]:
            self.isexpand = True
            self.ischecked = True
        else:
            self.ischecked = False
            self.isexpand = False
        return gid