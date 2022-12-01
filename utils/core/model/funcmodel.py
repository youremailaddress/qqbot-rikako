from utils.core.model import *

class Func(Base):
    __tablename__ = "func"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    name = Column(String(32), unique=True,nullable=False)
    usage = Column(String(256),nullable=False)
    intro = Column(String(256),nullable=False)
    istimer = Column(String(2),nullable=False)
    paramstring = Column(String(512),nullable=False)

    def __repr__(self) -> str:
        return f"功能id：{self.id}，功能名：{self.name}，功能用法：{self.usage}，功能介绍：{self.intro}"