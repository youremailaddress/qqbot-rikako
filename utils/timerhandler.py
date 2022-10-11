from utils.dbhandler import DbHandler
from utils.model import *
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.matcher import Matcher
from nonebot import get_driver
import time as tm
import json
from utils.permissionhandler import User
driver = get_driver()
global_config = get_driver().config

class Timi:
    def __init__(self,start:str,interval=None) -> None:
        if interval == None:
            assert len(start.split("_")) == 2
            self.start = start.split("_")[0]
            self.interval = start.split("_")[1]
        else:
            self.start = start
            self.interval = interval
        res = self._correctCheck()
        if res == False:
            assert False
        
    def __repr__(self) -> str:
        return f"开始于{tm.strftime('%Y/%m/%d %H:%M',tm.localtime(self.start))},间隔为{self.interval//86400}天{(self.interval%86400)//3600}小时{((self.interval%86400)%3600)//60}分钟"

    def _correctCheck(self) -> bool:
        if not self.start.isdigit() or not self.interval.isdigit():
            return False
        self.start = int(self.start)
        self.interval = int(self.interval)
        return True

    def _is_same(self,time1,time2) -> bool:
        tm1 = tm.localtime(time1)
        tm2 = tm.localtime(time2)
        if tm1.tm_year == tm2.tm_year and tm1.tm_mon == tm2.tm_mon and tm1.tm_mday == tm2.tm_mday and tm1.tm_hour== tm2.tm_hour and tm1.tm_min == tm2.tm_min:
            return True
        else:
            return False

    def _parsetime(self,time:int) -> bool:
        if self.interval == 0:
            return self._is_same(self.start,time)
        else:
            reslis = [self._is_same(self.start+k*self.interval,time) for k in range((time-60-self.start)//self.interval,(time+60-self.start)//self.interval+1)]
            if True in reslis:
                return True
            else:
                return False

class TimerHandler(DbHandler):
    # timer 的作用其实就是掌管调度器，每次调度的时候确定哪个函数应该怎么执行
    # 定时执行的函数一般情况下普遍具有的特征有：需要 bot 发送消息，需要发送的人物/群组，在什么时间/间隔发送，要生成发送的消息需要什么参数
    # 需要在底层进行一些限制，比如不能允许给别人或者别的群发送骚扰性质的定时任务，所以需要记录是谁 obtain this record,限制个数并且允许其handle
    # 需要讨论的是：是否要记录发送时所在群聊？ 或者单纯添加时判断
    # 不需要记录群聊，当时判断即可
    def __init__(self):
        super().__init__('/utils/timers.db', TimerBase)

    def _register(self,func_name,func_intro) -> bool:
        res = self.session.query(Time).filter(Time.name==func_name).first()
        if res != None:
            return True
        else:
            self.session.add(Time(name=func_name,intro=func_intro))
            self.session.commit()
            return True
    
    def _checker(self,funcname,time):
        if global_config.set_on == False: # 如果关机状态不响应任何使用本checker的命令
            return False
        Schedulelis = self.session.query(Schedule).join(Time).filter(Time.name==funcname).all()
        res = [(Timi(i.times)._parsetime(time),User(i.users),i.params) for i in Schedulelis]
        retval = []
        for item in res:
            if item[0] == True:
                tempdic = json.loads(item[2])
                tempdic['uid'] = item[1].uid if item[1].uid not in ["*","#1","#2","#3","#4"] else None
                tempdic['gid'] = item[1].gid if item[1].gid not in ["*","@"] else None
                if tempdic["uid"] == None and tempdic["gid"] == None:
                    continue
                if tempdic["uid"] != None and tempdic["gid"] != None:
                    continue
                retval.append(tempdic)
        if retval == []:
            return False
        else:
            return retval

    def checker(self,info):
        def decorator(func):
            self._register(func.__name__,info)
            async def wrapper(bot:Bot):
                res = self._checker(func.__name__,int(tm.time()))
                if res == False:
                    return False
                else:
                    for item in res:
                        await func(bot,**item)
            return wrapper
        return decorator

    def addTime(self,funcname,time,uid,gid,obtaineduid,**kwargs):
        # funcname:timer函数的名字
        # time:必须是 start_interval 格式
        # gid/uid 必须是满足User要求的
        # obtaineduid 必须是合法qq号
        # 返回值为 False 的原因：没有这个timer 或者 超出配额
        func = self.session.query(Time).filter(Time.name==funcname).one()
        if func == None:
            return False
        funcid = func.id
        if self.checkUsage(obtaineduid) == True:
            self.session.add(Schedule(tid=funcid,times=time,users=str(User(gid,uid)),obtaineduid=obtaineduid,params=json.dumps(kwargs)))
            self.session.commit()
        else:
            return False

    def checkUsage(self,obtaineduid):
        # 一个人最多可以有25条定时任务
        count = self.session.query(Schedule).filter(Schedule.obtaineduid==obtaineduid).count()
        if count > 25:
            return False
        else:
            return True
    
    def viewUsage(self,obtaineduid) -> str:
        # 本身不做权限设置 handler外的perm也只是决定谁可以触发，更细粒度的权限设置要在handler里设定
        count = self.session.query(Schedule).filter(Schedule.obtaineduid==obtaineduid).count()
        if count == 0:
            return "定时任务用量:0"
        else:
            res = self.session.query(Schedule).filter(Schedule.obtaineduid==obtaineduid).all()
            retval = f"定时任务用量:{count}\n"
            for item in res:
                retval += f"定时任务id:{item.id} 定时函数名:{item.timer.name} {str(Timi(item.times))} 设定给{item.users}发送\n"
            return retval[:-1]
    
    def RemoveUsage(self,obtaineduid,id):
        # 只有本人才能删自己设定的定时任务
        wait = self.session.query(Schedule).filter(Schedule.id == id).one()
        if wait == None or wait.obtaineduid != obtaineduid:
            return False
        else:
            self.session.query(Schedule).filter(Schedule.id == id).delete()
            self.session.commit()
            return True

TMH = TimerHandler()