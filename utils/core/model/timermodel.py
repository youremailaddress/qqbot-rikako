from utils.core.model import *

class Time(Base):
    __tablename__ = "timer"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True,nullable=False) # 定时任务 id
    fid = Column(Integer, ForeignKey('func.id')) # 函数 id
    func = relationship("Func",backref=backref('frole', lazy='joined'))
    uid = Column(String(16),nullable=False) # 单纯 uid 非扩展
    start = Column(Integer,nullable=False) # 开始时间 秒单位时间戳
    interval = Column(Integer,nullable=False) # 间隔时间 秒单位时间戳 无重复为 0
    pid = Column(Integer, ForeignKey('personalize.id')) # 个性化 id
    person = relationship("Personalize",backref=backref('ptime', lazy='joined'))