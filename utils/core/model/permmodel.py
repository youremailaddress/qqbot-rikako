from utils.core.model import *

class Func_User(Base):
    __tablename__ = "func_user"
    __table_args__ = {'extend_existing': True}
    fid = Column(Integer, ForeignKey('func.id'),primary_key=True) # 函数 id 
    func = relationship("Func",backref=backref('fuser', lazy='joined'))
    uid = Column(String(16),nullable=False,primary_key=True) # 用户 uid 取值为 [*,#1,#2,#3,#4,num] 内置了几种扩展 uid *为任意 #1-#4 依次为 群主、管理、群员、匿名
    gid = Column(String(16),nullable=False,primary_key=True) # 群组 gid 取值为 [@,*,num] 扩展的gid @即私聊，*为任意群聊

class Disable(Base):
    __tablename__ = "disable"
    __table_args__ = {'extend_existing': True}
    fid = Column(Integer, ForeignKey('func.id'),primary_key=True)
    uid = Column(String(16),nullable=False,primary_key=True) # 用户 uid 取值为 [*,#1,#2,#3,#4,num] 内置了几种扩展 uid *为任意 #1-#4 依次为 群主、管理、群员、匿名
    gid = Column(String(16),nullable=False,primary_key=True) # 群组 gid 取值为 [@,*,num] 扩展的gid @即私聊，*为任意群聊
    func = relationship("Func",backref=backref('dfuser', lazy='joined'))