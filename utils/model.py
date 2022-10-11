from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.orm import relationship,backref
PermBase = declarative_base()
TimerBase = declarative_base()

class Func(PermBase):
    __tablename__ = "func"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True,nullable=False)
    name = Column(String(32),nullable=False,unique=True)
    usage = Column(String(144),nullable=False)
    intro = Column(String(256),nullable=False)

    def __repr__(self) -> str:
        return f"功能id：{self.id}，功能名：{self.name}，功能用法：{self.usage}，功能介绍：{self.intro}"

class Role(PermBase):
    __tablename__ = "role"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True,nullable=False)
    name = Column(String(32),nullable=False,unique=True)

    def __repr__(self) -> str:
        return f"角色id：{self.id}，角色名称：{self.name}"

class Role_User(PermBase):
    __tablename__ = "role_user"
    __table_args__ = {'extend_existing': True}
    rid = Column(Integer, ForeignKey('role.id'),primary_key=True)
    role = relationship('Role',backref=backref('users', lazy='joined'))
    uid = Column(String(32),nullable=False,primary_key=True)

    def __repr__(self) -> str:
        return f"角色id：{self.rid}，角色名：{self.role.name}，包含用户：{self.uid}" # todo:find a more instant way to show users 

class Func_Role(PermBase):
    __tablename__ = "func_role"
    __table_args__ = {'extend_existing': True}
    fid = Column(Integer, ForeignKey('func.id'),primary_key=True)
    rid = Column(Integer, ForeignKey('role.id'),primary_key=True)
    func = relationship("Func",backref=backref('frole', lazy='joined'))
    role = relationship("Role",backref=backref('rfunc', lazy='joined'))

    def __repr__(self) -> str:
        return f"fid:{self.fid},rid:{self.rid}"

class Disable(PermBase):
    __tablename__ = "disable"
    __table_args__ = {'extend_existing': True}
    fid = Column(Integer, ForeignKey('func.id'),primary_key=True)
    rid = Column(Integer, ForeignKey('role.id'),primary_key=True)
    func = relationship("Func",backref=backref('froledis', lazy='joined'))
    role = relationship("Role",backref=backref('rfuncdis', lazy='joined'))

class Time(TimerBase):
    __tablename__ = "timer"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True,nullable=False)
    name = Column(String(32),nullable=False,unique=True)
    intro = Column(String(256),nullable=False)

class Schedule(TimerBase):
    __tablename__ = "schedule"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True,nullable=False)
    tid = Column(Integer, ForeignKey('timer.id'))
    timer = relationship('Time',backref=backref('schedule', lazy='joined'))
    obtaineduid = Column(String(16),nullable=False)
    times = Column(String(64),nullable=False)
    # 格式形如 start_interval 单位是second
    users = Column(String(32),nullable=False)
    # 格式和 perm 里的 user 相同
    params = Column(String(512))