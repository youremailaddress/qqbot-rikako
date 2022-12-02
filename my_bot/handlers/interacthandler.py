from my_bot.handlers.utils import *
from utils.core.tools.jsonconf import Jsonify
from utils.core.tools.time import TimeUnit
from utils.core.tools.user import Unit
from my_bot.handlers.eventparser import EventGURParser
from utils.core.cache.cache import CacheHwd
import utils.conf.confparser
import os
import time as timemodule
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.matcher import Matcher
from nonebot import get_driver
driver = get_driver()
global_config = get_driver().config

class BotHandler():
    def __init__(self) -> None:
        self.func = FunctionHandler()
        self.conf = ConfHandler()
        self.perm = PermissionHandler()
        self.timer = TimerHandler()
    
    def _register(self,name,intro,usage,paramstring="{}",istimer=False):
        self.func.register(name,intro,usage,istimer,paramstring)

    def addPerm(self,funcname:str,uid:str,gid:str,isblack=False):
        fid = self.func.getFuncid(funcname)
        if fid == False:
            return False
        try:
            Unit(uid,gid)
        except:
            return False
        return self.perm.add_perm(fid,uid,gid,isblack)

    def delPerm(self,funcname:str,uid:str,gid:str,isblack=False):
        fid = self.func.getFuncid(funcname)
        if fid == False:
            return False
        try:
            Unit(uid,gid)
        except:
            return False
        return self.perm.del_perm(fid,uid,gid,isblack)

    def _work_checker(self):
        # 检查是否开机
        if global_config.set_on == False: # 如果关机状态不响应任何使用本checker的命令
            return False
        return True
    
    def _perm_checker(self,name:str,uid:str,gid:str,role:str):
        '''
        gid:None or str
        role:None or str
        '''
        Neg = self.perm.get_Func_Perm(name,isblack=True)
        for unit in Neg:
            if (uid,gid,role) in unit:
                return False
        Pos = self.perm.get_Func_Perm(name,isblack=False)
        for unit in Pos:
            if (uid,gid,role) in unit:
                return True
        return False
    
    def _time_checker(self,name:str,time:int):
        '''
        判断在time时某函数是否该被执行，返回个性化(uid,gid,pid)列表
        '''
        res = self.timer.get_timer_by_name(name)
        retval = []
        for uid,gid,start,interval,pid in res:
            if time in TimeUnit(start,interval):
                retval.append((uid,gid,pid))
        return retval
    
    def _conf_checker(self,fid:int,uid:str,pid:int=None):
        '''
        :conf 正确性检查 pid 为 optional 
        :如果为空则尝试寻找该 func / uid 的 main_conf 
        :返回已经处理好的 param dic OR False
        '''
        paramstr = self.func.getParamstring(fid)
        if paramstr == None:
            return False
        if pid != None: # 给了 pid
            if not self.conf.Match(uid,pid): # 必须是本人的conf
                return False
            confstr = self.conf.getConf(pid)
            if confstr == None:
                return False
            res = Jsonify(paramstr).preParamProcess(confstr)
            if res == None:
                return False
            else:
                return res
        else:
            if self.conf.has_main_conf(fid,uid):
                confstr = self.conf.get_main_conf(fid,uid)[4]
                if confstr == None:
                    return False
                res = Jsonify(paramstr).preParamProcess(confstr)
                if res == None:
                    return False
                else:
                    return res
            else:
                return {}
        
    def _on_event_checker(self,name:str,uid:str,gid:str,role:str):
        '''
        on event 函数 执行前的检查 返回 params dic OR False
        '''
        if not self._work_checker():
            return False
        fid = self.func.getFuncid(name)
        if fid == False:
            return False
        if not self._perm_checker(name,uid,gid,role):
            return False
        else:
            return self._conf_checker(fid,uid)
    
    def _time_exec_checker(self,name:str,time:int):
        '''
        执行前的检查 针对 timer 函数 返回列表 [(uid,gid,params dic)]
        '''
        if not self._work_checker():
            return []
        fid = self.func.getFuncid(name)
        if fid == False:
            return []
        a = self._time_checker(name,time)
        res = []
        for _uid,_gid,_pid in a:
            conf = self._conf_checker(fid,_uid,_pid)
            if conf == False:
                continue
            res.append((_uid,_gid,conf))
        return res

    def _add_timer_checker(func):
        '''
        在添加 timer 的时候进行的权限检查
        '''
        def decorator(self,name:str,uid:str,gid:str,start:int,interval:int,pid:int):
            # 如何检查 timer
            un = Unit(uid,gid)
            if un.uid.isexpand or un.gid.isexpand:
                return False
            if not self._perm_checker(name,uid,gid,CacheHwd.get_role(uid,gid)):
                return False
            return func(self,name,uid,gid,start,interval,pid)
        
        return decorator

    def checker(self,name,usage,intro,istimer=False,req=[],optional=[],isAdmin=False):
        self._register(name,usage,intro,Jsonify.wrapReqOpt(req,optional),istimer)
        if isAdmin:
            self.addPerm(name,os.getenv("SUPER"),"*")
            self.addPerm(name,os.getenv("SUPER"),"@")
        def decorator(func):
            if not istimer: # 如果是 on event 函数
                async def wrapper(bot: Bot, event: Event, state: T_State,matcher: Matcher):
                    GUR = EventGURParser(event)
                    res = self._on_event_checker(name,GUR.uid,GUR.gid,GUR.role)
                    if res == False:
                        return False
                    else:
                        await func(bot,event, state,matcher,**res)
                    
            else:
                async def wrapper(bot: Bot,**kwargs):
                    res = self._time_exec_checker(name,int(timemodule.time()))

                    for uid,gid,item in res:
                        await func(bot,uid,gid,**item)
            return wrapper
        return decorator  

    @_add_timer_checker
    def addTimer(self,name:str,uid:str,gid:str,start:int,interval:int,pid:int):
        if self.conf.getConf(pid) == None:
            return False
        fid = self.func.get_id_by_name(name)
        return self.timer.add_timer(fid,uid,gid,start,interval,pid)
    
BH = BotHandler()