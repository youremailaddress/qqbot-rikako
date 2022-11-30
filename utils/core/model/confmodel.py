from utils.core.model import *

class Personalize(Base):
    __tablename__ = "personalize"
    __table_args__ = (
        UniqueConstraint("fid","uid","params"),
        {'extend_existing': True}
        )
    id = Column(Integer, primary_key=True, autoincrement=True,nullable=False) # 个性化id
    fid = Column(Integer, ForeignKey('func.id')) # 函数 id
    func = relationship("Func",backref=backref('fperson', lazy='joined'))
    uid = Column(String(16),nullable=False) # 创建和使用个性化设置的 uid 必须是数字，不能是扩展类型
    params = Column(String(512)) # 个性化设置
    isdefault = Column(String(2)) # 不是很好的设计 需要保证 fid & uid 相同的若干设置存在小于等于一个的默认设置
