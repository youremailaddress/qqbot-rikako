from nonebot.adapters.cqhttp import Event
class EventGURParser():
    '''
    从 event 中解析 Gid / Uid / Role
    '''
    def __init__(self,event:Event) -> None:
        self.gid,self.uid,self.role = self.Parse(event)

    def Parse(self,event:Event):
        groupid = None
        uid = event.get_user_id()
        try:
            role = event.sender.role
        except:
            role = None
        if len(event.get_session_id().split("_"))>1:
            groupid = event.get_session_id().split("_")[1]
        return (groupid,uid,role)