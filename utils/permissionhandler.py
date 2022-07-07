from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp.event import *
from nonebot import get_driver
from utils.dbhandler import SelfDefineDBHandler
driver = get_driver()
global_config = get_driver().config

class PermissionDBHandler(SelfDefineDBHandler):
    def __init__(self, path=global_config.root+"utils/permissions.db"):
        super().__init__(path)
    
    def push(self,tablename,config,sql,data):
        db,cursor = self._ensureTable(tablename,config)
        try:
            cursor.execute(sql,data)
            db.commit()
            db.close()
            return True
        except Exception as e:
            print(str(e))
            db.rollback()
            db.close()
            return False
    
    def pushmany(self,tablename,config,sql,datalis):
        db,cursor =self._ensureTable(tablename,config)
        try:
            cursor.executemany(sql,datalis)
            db.commit()
            db.close()
            return True
        except:
            db.rollback()
            db.close()
            return False

    def getone(self,tablename,config,sql,data):
        db,cursor =self._ensureTable(tablename,config)
        try:
            cursor.execute(sql,data)
            a = cursor.fetchone()
            db.close()
            if a != None:
                return a[0]
            else:
                return None
        except Exception as e:
            print(str(e))
            db.close()
            return False
    
    def getmany(self,tablename,config,sql,data):
        db,cursor =self._ensureTable(tablename,config)
        try:
            cursor.execute(sql,data)
            a = cursor.fetchall()
            db.close()
            return a
        except Exception as e:
            print(str(e))
            db.close()
            return False

class PermissionHandler():
    def __init__(self,funcname,funcusage,funcintro) -> None:
        self.dbh = PermissionDBHandler()
        self.cfg = {
            "role_table":[("role_id","Integer","PRIMARY KEY AUTOINCREMENT NOT NULL"),("role_name","TEXT","UNIQUE NOT NULL")],
            "role_user_table":[("role_id","Integer","NOT NULL"),("user_id","TEXT","NOT NULL")],
            "func_table":[("func_id","Integer","PRIMARY KEY AUTOINCREMENT NOT NULL"),("func_name","TEXT","UNIQUE NOT NULL"),("func_usage","TEXT","NOT NULL"),("func_intro","TEXT","NOT NULL")],
            "func_role_table":[("func_id","Integer","NOT NULL"),("role_id","Integer","NOT NULL")],
            "disable_table":[("func_id","Integer","NOT NULL"),("role_id","Integer","NOT NULL")]
        }
        self.funcname = funcname
        self.funcusage = funcusage
        self.funcintro = funcintro
        for k,v in self.cfg.items():
            self.dbh._ensureTable(k,v)
        self.register()
    
    def isOfGroup(self,event):
        '''
        查看是否是和Group相关的事件
        '''
        return isinstance(event,GroupMessageEvent) or isinstance(event,GroupAdminNoticeEvent) or isinstance(event,GroupBanNoticeEvent) or isinstance(event,GroupDecreaseNoticeEvent) or isinstance(event,GroupIncreaseNoticeEvent) or isinstance(event,GroupRecallNoticeEvent) or isinstance(event,GroupRequestEvent) or isinstance(event,GroupUploadNoticeEvent)

    def register(self):
        '''
        在数据库里查询是否注册func，若没有则注册
        '''
        sql = '''select func_id from func_table where func_name = ?;'''
        res = self.dbh.getone("func_table",self.cfg["func_table"],sql,(self.funcname,))
        if res != None:
            return True
        else:
            sqlinsert = '''insert into func_table(func_name,func_usage,func_intro) values (?,?,?);'''
            self.dbh.push("func_table",self.cfg["func_table"],sqlinsert,(self.funcname,self.funcusage,self.funcintro))
            return True

    def _parseUser(self,User,uid,gid,role):
        '''
        判断一个 uid + gid 是不是在 User 的辖域内
        User 是 数据库里的 uid 是 获取的 QQ 号， gid 是可能存在的群号，role是可能存在的群角色[owner,admin,member,None]
        '''
        user = User.split("_")
        assert len(user) == 2
        if (user[0] == '*'): # 任意群聊
            if gid == None: # 私聊
                return False
            if (user[1] == '*'): # 如果是任意人,恒真
                return True
            elif (user[1] == '#1'):  # 如果是任意群主
                if role == 'owner':
                    return True
                else:
                    return False
            elif (user[1] == '#2'): # 如果是任意管理
                if role == 'admin':
                    return True
                else:
                    return False
            elif (user[1] == '#3'): # 如果是任意成员
                if role == 'member':
                    return True
                else:
                    return False
            elif (user[1] == '#4'): # 如果是任意匿名用户
                if role == None and uid == '80000000':
                    return True
                else:
                    return False
            else:                # 如果是任意群聊指定人
                if uid == user[1]:
                    return True
                else:
                    return False
        elif (user[0] == '@'): # 私聊
            if gid != None: # 群聊
                return False
            if (user[1] == '*'): # 如果是任意人,恒真
                return True
            else:
                if uid == user[1]:
                    return True
                else:
                    return False
        else:
            if gid != user[0]:
                return False
            if (user[1] == '*'): # 如果是任意人,恒真
                return True
            elif (user[1] == '#1'):  # 如果是群主
                if role == 'owner':
                    return True
                else:
                    return False
            elif (user[1] == '#2'): # 如果是管理
                if role == 'admin':
                    return True
                else:
                    return False
            elif (user[1] == '#3'): # 如果是成员
                if role == 'member':
                    return True
                else:
                    return False
            elif (user[1] == '#4'): # 如果是匿名用户
                if role == None and uid == '80000000':
                    return True
                else:
                    return False
            else:                # 如果是群聊指定人
                if uid == user[1]:
                    return True
                else:
                    return False

    def _inDisTable(self,uid,gid,fid,role):
        '''
        如果在 distable 里，返回 True
        如果不在 distable 里，返回 False
        '''
        sql = '''select user_id from role_user_table,disable_table where disable_table.func_id = ? and role_user_table.role_id = disable_table.role_id;'''
        res = self.dbh.getmany("disable_table",self.cfg["disable_table"],sql,(fid,))
        if res == None:
            return False
        for item in res:
            item = item[0]
            if (self._parseUser(item,uid,gid,role)==True):
                return True
        return False

    def _inWhiteList(self,uid,gid,fid,role):
        '''
        是否在白名单里，如果在返回 True
        不在 返回 False
        '''
        sql = '''select user_id from role_user_table,func_role_table where func_id = ? and func_role_table.role_id = role_user_table.role_id;'''
        res = self.dbh.getmany("role_user_table",self.cfg["role_user_table"],sql,(fid,))
        if res == None:
            return False
        for item in res:
            item = item[0]
            if (self._parseUser(item,uid,gid,role)):
                return True
        return False

    def async_checker(self, bot: Bot, event: Event) -> bool:
        '''
        权限检查函数 v1
        '''
        if global_config.set_on == False: # 如果关机状态不响应任何使用本checker的命令
            return False
        groupid = None
        uid = event.get_user_id()
        try:
            role = event.sender.role
        except:
            role = None
        if self.isOfGroup(event):
            groupid = event.get_session_id().split("_")[1]
        # 查找 func 对应 func_id       
        sql = '''select func_id from func_table where func_name=?'''
        func_id = self.dbh.getone("func_table",self.cfg["func_table"],sql,(self.funcname,))
        assert func_id != None
        # 如果该用户在 disable_table 里面不响应 
        if self._inDisTable(uid,groupid,func_id,role):
            return False
        # 如果该用户在 白名单 里 响应
        if self._inWhiteList(uid,groupid,func_id,role):
            return True
        # 默认策略是 False
        return False

    def checkUserParse(self,user):
        '''
        检查权限 user 是否符合格式条件
        '''
        user = user.split("_")
        if len(user) != 2:
            return False
        if user[0] == '*' and user[1] in ['*','#1','#2','#3','#4']:
            return True
        if user[0] == '@' and user[1] == '*':
            return True
        if user[0] in ['*','@'] and user[1].isdigit():
            return True
        if user[0].isdigit() and user[1].isdigit():
            return True
        if user[0].isdigit() and user[1] in ['*','#1','#2','#3','#4']:
            return True
        return False
    