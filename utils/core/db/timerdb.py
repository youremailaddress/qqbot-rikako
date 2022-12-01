from utils.core.db import *

class TimerDB(FuncDB):
    def __init__(self) -> None:
        super().__init__()

    def add_timer(self,fid:int,uid:int,gid:int,start:int,interval:int,pid:int):
        '''
        add_timer:添加 timer
        fid:验证过存在的fid
        uid:验证过未扩展的uid
        start/interval:时间戳
        pid:验证过的个性化id
        '''
        try:
            self.session.add(Time(fid=fid,uid=str(uid),gid=str(gid),start=start,interval=interval,pid=pid))
            self.session.commit()
            return True
        except:
            self.session.rollback()
            return False
    

    def del_timer_by_id(self,id:int):
        '''
        del_timer_by_id:删除定时任务
        '''
        try:
            self.session.query(Time).filter(Time.id==id).delete()
            self.session.commit()
            return True
        except:
            self.session.rollback()
            return False

    def select_timer_by_id(self,id:int):
        '''
        select_timer_by_id:根据 id 查询定时任务
        return:None or (a.fid,a.func.name,a.uid,a.gid,a.start,a.interval,a.pid,a.person.params)
        '''
        a = self.session.query(Time).filter(Time.id==id).one()
        if a == None:
            return None
        else:
            return (a.fid,a.func.name,a.uid,a.gid,a.start,a.interval,a.pid,a.person.params)

    def select_timer_by_user(self,uid:int):
        '''
        select_timer_by_user:根据 uid 查询定时任务
        return:列表
        '''
        a = self.session.query(Time).filter(Time.uid==int(uid)).all()
        if a == []:
            return []
        else:
            return [(i.fid,i.func.name,i.uid,i.gid,i.start,i.interval,i.pid,i.person.params) for i in a]

    def select_timer_by_name(self,name:str):
        a = self.session.query(Time).join(Func).filter(Func.name == name).all()
        if a == []:
            return []
        else:
            return [(i.fid,i.func.name,i.uid,i.gid,i.start,i.interval,i.pid,i.person.params) for i in a]