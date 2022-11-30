from my_bot.handlers.utils import *
from utils.core.tools.user import Unit
from nonebot import get_driver
driver = get_driver()
global_config = get_driver().config

class BotHandler():
    def __init__(self) -> None:
        self.func = FunctionHandler()
        self.conf = ConfHandler()
        self.perm = PermissionHandler()
        self.timer = TimerHandler()
    
    def _register(self,name,intro,usage,istimer=False):
        self.func.register(name,intro,usage,istimer)

    def _work_checker(self):
        # 检查是否开机
        if global_config.set_on == False: # 如果关机状态不响应任何使用本checker的命令
            return False
        return True
    
    def _perm_checker(self,name,uid,gid,role):
        Neg = self.perm.get_Func_Perm(name,isblack=True)
        for unit in Neg:
            if (uid,gid,role) in unit:
                return False
        Pos = self.perm.get_Func_Perm(name,isblack=False)
        for unit in Pos:
            if (uid,gid,role) in unit:
                return True
        return False
    
    def _time_checker(self,name,time):
        pass
