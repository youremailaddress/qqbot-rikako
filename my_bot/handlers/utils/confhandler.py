from utils.core.db.confdb import ConfigDB

class ConfHandler(ConfigDB):
    def __init__(self) -> None:
        super().__init__()

    def Match(self,uid:str,pid:int):
        res = self.get_conf_by_id(pid)
        if res == None:
            return False
        elif res[3] == str(uid):
            return True
        else:
            return False
    
    def getConf(self,pid:int):
        a = self.get_conf_by_id(pid)
        if a == None:
            return None
        else:
            return a[4]