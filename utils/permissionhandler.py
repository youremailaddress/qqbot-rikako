from utils.dbhandler import DbHandler
from utils.model import *
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.matcher import Matcher
from nonebot import get_driver
from utils.functions import getDir
driver = get_driver()
global_config = get_driver().config


class User:
    def __init__(self,gid:str,uid=None) -> None:
        '''
        init from two parts or __repr__ is ok
        User.gid can be *,@,groupid
        User.uid can be *,#1,#2,#3,#4,userid
        '''
        if uid==None:
            assert len(gid.split("_")) == 2
            self.gid = gid.split("_")[0]
            self.uid = gid.split("_")[1]
        else:
            self.gid = gid
            self.uid = uid
        assert self._correctCheck()

    def __repr__(self) -> str:
        return f"{self.gid}_{self.uid}"

    def _correctCheck(self) -> bool:
        '''
        check if user is vaild,if it is,return True
        '''
        if not self.uid.isdigit() and self.uid not in ["*","#1","#2","#3","#4"]:
            return False
        if self.gid=="@" and self.uid in ["#1","#2","#3","#4"]:
            return False
        if not self.gid.isdigit() and self.gid not in ["*","@"]:
            return False
        return True

    def _parseuser(self,uid,gid,role) -> bool:
        '''
        given uid,gid,role check if a user contains this pattern.
        '''
        if self.gid == '*':# 任意群聊
            if gid == None: # 私聊
                return False
            if (self.uid == '*'):# 如果是任意人,恒真
                return True
            elif (self.uid == '#1'):  # 如果是任意群主
                if role == 'owner':
                    return True
                else:
                    return False
            elif (self.uid == '#2'): # 如果是任意管理
                if role == 'admin':
                    return True
                else:
                    return False
            elif (self.uid == '#3'): # 如果是任意成员
                if role == 'member':
                    return True
                else:
                    return False
            elif (self.uid == '#4'): # 如果是任意匿名用户
                if role == None and uid == '80000000':
                    return True
                else:
                    return False
            else:                # 如果是任意群聊指定人
                if uid == self.uid:
                    return True
                else:
                    return False
        elif (self.gid == '@'): # 私聊
            if gid != None: # 群聊
                return False
            if (self.uid == '*'): # 如果是任意人,恒真
                return True
            else:
                if uid == self.uid:
                    return True
                else:
                    return False
        else:
            if gid != self.gid:
                return False
            if (self.uid == '*'): # 如果是任意人,恒真
                return True
            elif (self.uid == '#1'):  # 如果是群主
                if role == 'owner':
                    return True
                else:
                    return False
            elif (self.uid == '#2'): # 如果是管理
                if role == 'admin':
                    return True
                else:
                    return False
            elif (self.uid == '#3'): # 如果是成员
                if role == 'member':
                    return True
                else:
                    return False
            elif (self.uid == '#4'): # 如果是匿名用户
                if role == None and uid == '80000000':
                    return True
                else:
                    return False
            else:                # 如果是群聊指定人
                if uid == self.uid:
                    return True
                else:
                    return False

class PermissionHandler(DbHandler):
    def __init__(self) -> None:
        super().__init__(getDir("databases/permissions.db"),PermBase)

    def _register(self,func_name,func_usage,func_intro) -> bool:
        '''
        if a plugin-method is not registered,then add it to permission database func table 
        '''
        res = self.session.query(Func.name).filter_by(name=func_name).first()
        if res != None:
            return True
        else:
            newfunc=Func(name=func_name,usage=func_usage,intro=func_intro)
            self.session.add(newfunc)
            self.session.commit()
            return True

    def register(self,name,usage,intro):
        def decorator(func):
            self._register(name,"[SUPER]"+usage,intro)
            def wrapper(bot: Bot, event: Event, state: T_State,matcher: Matcher):
                return func(bot, event, state,matcher)
            return wrapper
        return decorator

    def _parseUser(self,user,uid,gid,role):
        '''
        User 
        '''
        pass

    def _checker(self,funcname,uid,gid,role):
        if global_config.set_on == False: # 如果关机状态不响应任何使用本checker的命令
            return False
        Dis = self.session.query(Disable).join(Func).join(Func_Role).filter(Func.name==funcname).all()
        disCheckList = [User(item.rfuncdis)._parseuser(uid,gid,role) for item in Dis]
        if True in disCheckList:
            return False
        RUser = self.session.query(Role_User).join(Role).join(Func_Role).join(Func).filter(Func.name==funcname).all()
        checkList = [User(item.uid)._parseuser(uid,gid,role) for item in RUser]
        if True in checkList:
            return True
        else:
            return False

    def checker(self,name,usage,intro):
        self._register(name,usage,intro)
        def decorator(func):
            def wrapper(bot: Bot, event: Event, state: T_State,matcher: Matcher):
                groupid = None
                uid = event.get_user_id()
                try:
                    role = event.sender.role
                except:
                    role = None
                if len(event.get_session_id().split("_"))>1:
                    groupid = event.get_session_id().split("_")[1]
                if self._checker(name,uid,groupid,role):
                    return func(bot, event, state,matcher)
                else:
                    return False
                    
            return wrapper
        return decorator

PMH = PermissionHandler()