from my_bot.handlers.utils import *
from utils.core.tools.jsonconf import Jsonify
from utils.core.tools.time import TimeUnit
from my_bot.handlers.eventparser import EventGURParser
import json
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
    
    def _register(self,name,intro,usage,paramstring,istimer=False):
        self.func.register(name,intro,usage,istimer,paramstring)

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
        if pid != None: # 给了 pid
            if not self.conf.Match(uid,pid): # 必须是本人的conf
                return False
            paramstr = self.func.getParamstring(fid)
            if paramstr == None:
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
            # do something
            self.perm
            return func
        
        return decorator

    def checker(self,name,usage,intro,istimer,req,optional):
        self._register(name,usage,intro,Jsonify.wrapReqOpt(req,optional),istimer)
        def decorator(func):
            if not istimer: # 如果是 on event 函数
                async def wrapper(bot: Bot, event: Event, state: T_State,matcher: Matcher,**kwargs):
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
        self.timer.add_timer()