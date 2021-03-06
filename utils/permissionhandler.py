from typing import List
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
        ??????????????????Group???????????????
        '''
        return isinstance(event,GroupMessageEvent) or isinstance(event,GroupAdminNoticeEvent) or isinstance(event,GroupBanNoticeEvent) or isinstance(event,GroupDecreaseNoticeEvent) or isinstance(event,GroupIncreaseNoticeEvent) or isinstance(event,GroupRecallNoticeEvent) or isinstance(event,GroupRequestEvent) or isinstance(event,GroupUploadNoticeEvent)

    def register(self):
        '''
        ?????????????????????????????????func?????????????????????
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
        ???????????? uid + gid ???????????? User ????????????
        User ??? ??????????????? uid ??? ????????? QQ ?????? gid ???????????????????????????role???????????????????????????[owner,admin,member,None]
        '''
        user = User.split("_")
        assert len(user) == 2
        if (user[0] == '*'): # ????????????
            if gid == None: # ??????
                return False
            if (user[1] == '*'): # ??????????????????,??????
                return True
            elif (user[1] == '#1'):  # ?????????????????????
                if role == 'owner':
                    return True
                else:
                    return False
            elif (user[1] == '#2'): # ?????????????????????
                if role == 'admin':
                    return True
                else:
                    return False
            elif (user[1] == '#3'): # ?????????????????????
                if role == 'member':
                    return True
                else:
                    return False
            elif (user[1] == '#4'): # ???????????????????????????
                if role == None and uid == '80000000':
                    return True
                else:
                    return False
            else:                # ??????????????????????????????
                if uid == user[1]:
                    return True
                else:
                    return False
        elif (user[0] == '@'): # ??????
            if gid != None: # ??????
                return False
            if (user[1] == '*'): # ??????????????????,??????
                return True
            else:
                if uid == user[1]:
                    return True
                else:
                    return False
        else:
            if gid != user[0]:
                return False
            if (user[1] == '*'): # ??????????????????,??????
                return True
            elif (user[1] == '#1'):  # ???????????????
                if role == 'owner':
                    return True
                else:
                    return False
            elif (user[1] == '#2'): # ???????????????
                if role == 'admin':
                    return True
                else:
                    return False
            elif (user[1] == '#3'): # ???????????????
                if role == 'member':
                    return True
                else:
                    return False
            elif (user[1] == '#4'): # ?????????????????????
                if role == None and uid == '80000000':
                    return True
                else:
                    return False
            else:                # ????????????????????????
                if uid == user[1]:
                    return True
                else:
                    return False

    def _inDisTable(self,uid,gid,fid,role):
        '''
        ????????? distable ???????????? True
        ???????????? distable ???????????? False
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
        ??????????????????????????????????????? True
        ?????? ?????? False
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
        ?????????????????? v1
        '''
        if global_config.set_on == False: # ??????????????????????????????????????????checker?????????
            return False
        groupid = None
        uid = event.get_user_id()
        try:
            role = event.sender.role
        except:
            role = None
        if len(event.get_session_id().split("_"))>1:
            groupid = event.get_session_id().split("_")[1]
        # ?????? func ?????? func_id       
        sql = '''select func_id from func_table where func_name=?'''
        func_id = self.dbh.getone("func_table",self.cfg["func_table"],sql,(self.funcname,))
        assert func_id != None
        # ?????????????????? disable_table ??????????????? 
        if self._inDisTable(uid,groupid,func_id,role):
            return False
        # ?????????????????? ????????? ??? ??????
        if self._inWhiteList(uid,groupid,func_id,role):
            return True
        # ??????????????? False
        return False

    # def scheduled_job_hands_out(self,bot:Bot) -> List:
    #     '''
    #     ??????????????????????????????
    #     ?????? ?????? ?????? ??????
    #     '''
    #     if global_config.set_on == False: # ??????????????????????????????????????????checker?????????
    #         return []
    #     # ?????? func ?????? func_id       
    #     sql = '''select func_id from func_table where func_name=?'''
    #     func_id = self.dbh.getone("func_table",self.cfg["func_table"],sql,(self.funcname,))
    #     assert func_id != None
    #     sql = '''select user_id from role_user_table,func_role_table where func_id = ? and func_role_table.role_id = role_user_table.role_id;'''
    #     res = self.dbh.getmany("role_user_table",self.cfg["role_user_table"],sql,(func_id,))
    #     if res == None:
    #         return []
    #     res = [item[0] for item in res]
    #     sql = '''select user_id from role_user_table,disable_table where disable_table.func_id = ? and role_user_table.role_id = disable_table.role_id;'''
    #     resdis = self.dbh.getmany("disable_table",self.cfg["disable_table"],sql,(func_id,))
    #     if resdis == None:
    #         return res
    #     resdis = [item[0] for item in resdis]
    #     return list(set(res)-set(resdis))

    def checkUserParse(self,user):
        '''
        ???????????? user ????????????????????????
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

# schedule bot ????????????????????? PermissionHandler ???????????????????????????????????????????????????????????? schedule ?????????????????? schedule ?????????

# class ScheduleHandler():
#     def __init__(self,schedulename,scheduleusage,scheduleintro) -> None:
#         self.dbh = PermissionDBHandler()
#         self.cfg = {
#             "role_table":[("role_id","Integer","PRIMARY KEY AUTOINCREMENT NOT NULL"),("role_name","TEXT","UNIQUE NOT NULL")],
#             "role_user_table":[("role_id","Integer","NOT NULL"),("user_id","TEXT","NOT NULL")],
#             "schedule_table":[("schedule_id","Integer","PRIMARY KEY AUTOINCREMENT NOT NULL"),("schedule_name","TEXT","UNIQUE NOT NULL"),("schedule_usage","TEXT","NOT NULL"),("schedule_intro","TEXT","NOT NULL")],
#             "func_role_table":[("func_id","Integer","NOT NULL"),("role_id","Integer","NOT NULL")],
#             "disable_table":[("func_id","Integer","NOT NULL"),("role_id","Integer","NOT NULL")]
#         }
#         self.schedulename = schedulename
#         self.scheduleusage = scheduleusage
#         self.scheduleintro = scheduleintro
#         for k,v in self.cfg.items():
#             self.dbh._ensureTable(k,v)
#         self.register()

#     def register(self):
#         '''
#         ?????????????????????????????????func?????????????????????
#         '''
#         sql = '''select func_id from func_table where func_name = ?;'''
#         res = self.dbh.getone("func_table",self.cfg["func_table"],sql,(self.funcname,))
#         if res != None:
#             return True
#         else:
#             sqlinsert = '''insert into func_table(func_name,func_usage,func_intro) values (?,?,?);'''
#             self.dbh.push("func_table",self.cfg["func_table"],sqlinsert,(self.funcname,self.funcusage,self.funcintro))
#             return True