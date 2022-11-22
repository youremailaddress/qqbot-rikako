from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.orm import relationship,backref
CheckWordBase = declarative_base()

class CheckWord(CheckWordBase):
    __tablename__ = "checkword"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True,autoincrement=True,nullable=False)
    user = Column(Integer,nullable=False)
    check = Column(String(14),nullable=False)
    updatetime = Column(String(64),nullable=False)
    isused = Column(String(5),nullable=True)