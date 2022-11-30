from utils.db.dbhandler import DbHandler
from utils.core.model.model import *
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.matcher import Matcher
from nonebot import get_driver
import time as tm
import json
from os.path import exists
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
        # 判断两时间处于同一分钟内
        if int(time1)//60 == int(time2)//60:
            return True
        else:
            return False

    def _parsetime(self,time:int) -> bool:
        # 对比看看time是否在时间范围内
        if self.interval == 0:
            return self._is_same(self.start,time)
        else:
            reslis = [self._is_same(self.start+k*self.interval,time) for k in range((time-60-self.start)//self.interval,(time+60-self.start)//self.interval+1)]
            if True in reslis:
                return True
            else:
                return False

class FRIHandler():
    # 一个缓存机制 目的是方便 web 端进行鉴权
    # 里面存储了（最多一天内的）好友和群聊以及群聊中的人、角色对应关系
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
   
class FunctionHandler(DbHandler):
    # 把所有函数分为两类，事件驱动类和时间驱动类，前者是nonebot自带，后者是所谓定时任务
    # 这两个类型是完全独立的，如果一个功能既希望是事件驱动又希望是时间驱动，目前需要分开写
    # 所有函数都由权限控制，权限可以事件驱动类函数的执行与否，也可以决定时间驱动类函数的添加定时任务与否
    # 所有函数都可以是可定制的，可定制即允许根据不同人的不同设置在函数内部决定不同的处理方式，抽象到函数层面，即允许用户和函数参数的一对多对应
    def __init__(self) -> None:
        super().__init__(getDir("databases/func.db"),Base)
        self.fri = FRIHandler()

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
    
    def _work_checker(self):
        # 检查是否开机
        if global_config.set_on == False: # 如果关机状态不响应任何使用本checker的命令
            return False
        return True

    def _perm_checker(self,func_name,uid,gid,role):
        # 检查主体是否有权限执行函数（nonebot内置类型函数，对于定时任务，permchecker运行时无法找到其主体，因此permchecker对定时函数采用添加定时函数时check的办法处理）
        Dis = self.session.query(Disable).join(Func).filter(Func.name==func_name).all()
        # 先看黑名单再看白名单
        disCheckList = [User(item.uid)._parseuser(uid,gid,role) for item in Dis]
        if True in disCheckList:
            return False
        RUser = self.session.query(Func_User).join(Func).filter(Func.name==func_name).all()
        checkList = [User(item.uid)._parseuser(uid,gid,role) for item in RUser]
        if True in checkList:
            return True
        else:# 默认不放行
            return False
            
    def _time_checker(self,func_name,time):
        # 判断一个定时任务是否该被执行，返回的是个性化pid
        Schedulelis = self.session.query(Time).join(Func).filter(Func.name == func_name).all()
        res = [i.pid for i in Schedulelis if Timi(i.start,i.interval)._parsetime(time)]
        return res
        
    def _conf_checker(self,userid,pid):
        # 其实对参数内容的check我希望没有很硬性的标准，这样不同函数自由度会大一些，但是至少A不能使用B的参数，因此需要对调用的人做check
        return False if self.session.query(Personalize).filter(Personalize.id==pid,Personalize.userid==userid).count() == 0 else True

    def _add_time(self,func,uid,start,interval,pid):
        # 添加定时任务 
        # 首先要检查 uid 是否有 func 的执行权限
        canadd = False
        if not User(uid)._correctCheck() or User(uid).uid in ["*","#1","#2","#3","#4"]: # uid 不能是非法，userid 必须指定到个人
            return False
        if User(uid).gid == "@": # 如果是私聊的话，role是空 因此要单独拿出来写
            if self._perm_checker(func,User(uid).uid,User(uid).gid,None):
                canadd = True
        else: # 不是私聊的话，采用 cache 里缓存的数据确定 role
            for k,v in self.fri.get_gid_and_type(User(uid).uid):
                if k == User(uid).gid and self._perm_checker(func,User(uid).uid,k,v): # 必须是所在的群 必须在群里有对函数的权限
                    canadd = True
                    break
        if canadd:
            try:
                funcid = self.session.query(Func).filter(Func.name==func).one().id
                self.session.add(Time(fid=funcid,uid=uid,start=start,interval=interval,pid=pid))
                self.session.commit()
                return True
            except:
                return False
        return False

    def _del_time(self):
        # 
        pass

    def _show_time(self):
        pass

    def _in_perm(self,func,user,isblack=False):
        if isblack:
            M = Disable
        else:
            M = Func_User
        return True if self.session.query(M).join(Func).filter(Func.name == func,M.uid==user).count() > 0 else False

    def _add_perm(self,func,user,isblack=False):
        if isblack:
            M = Disable
        else:
            M = Func_User
        try:
            if not User(user)._correctCheck():
                return False
            else:
                if self._in_perm(func,user,isblack):
                    return False
                funcid = self.session.query(Func).filter(Func.name==func).one().id
                self.session.add(M(fid=funcid,uid=user))
                self.session.commit()
                return True
        except Exception as e:
            return False
    
    def _delete_perm(self,func,user,isblack=False):
        if isblack:
            M = Disable
        else:
            M = Func_User
        try:
            if not self._in_perm(func,user,isblack):
                return False
            else:
                funcid = self.session.query(Func).filter(Func.name==func).one().id
                self.session.query(M).filter(M.fid == funcid,M.uid==user).delete()
                self.session.commit()
                return True
        except:
            return False
    
    def _show_perm(self,isblack=False):
        if isblack:
            M = Disable
        else:
            M = Func_User
        reslis = self.session.query(M).join(Func).all()
        res = [ f"{item.func.name} {item.uid}" for item in reslis]
        return "\n".join(res)

    def _add_conf(self):
        pass

    def _del_conf(self):
        pass

    def _show_conf(self):
        pass

    def checker(self,name,usage,intro):
        self._register(name,usage,intro)
        def decorator(func):
            async def wrapper(bot: Bot, event: Event, state: T_State,matcher: Matcher):
                if not self._work_checker():
                    return False
                # 检查 是否 work
                if event != None:
                    groupid = None
                    uid = event.get_user_id()
                    try:
                        role = event.sender.role
                    except:
                        role = None
                    if len(event.get_session_id().split("_"))>1:
                        groupid = event.get_session_id().split("_")[1]
                    if not self._perm_checker(name,uid,groupid,role):
                        return False
                    else:
                        try:
                            a = self.session.query(Personalize).join(Func).filter(Func.name==name,Personalize.userid==uid).one()
                            item = json.loads(a.params)
                            await func(bot,event, state,matcher,**item)
                        except:
                            await func(bot,event, state,matcher)
                # 检查 perm
                else:
                    res = self._time_checker(name,int(tm.time()))
                    for single in res:
                        try:
                            a = self.session.query(Personalize).filter(Personalize.id==single).one()
                            item = json.loads(a.params)
                            await func(bot,event, state,matcher,uid=a.userid,**item)
                        except:
                            continue
            return wrapper
        return decorator
 

FunH = FunctionHandler()
