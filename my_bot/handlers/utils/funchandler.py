from utils.core.db.funcdb import FunctionDB

class FunctionHandler(FunctionDB):
    def __init__(self) -> None:
        super().__init__()
    
    def register(self,name:str,intro:str,usage:str,istimer:bool):
        return self.add_func(name,intro,usage,istimer)

    def getFuncid(self,name:str):
        return self.get_id_by_name(name)