from utils.db.dbhandler import DbHandler
from utils.path.pathparser import getDir
from utils.core.model import Base,Func_User,Disable,Time,Personalize,Func

class FuncDB(DbHandler):
    def __init__(self) -> None:
        super().__init__(getDir("databases/func.db"),Base)