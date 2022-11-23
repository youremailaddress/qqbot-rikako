from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.orm import relationship,backref
CheckWordBase = declarative_base()

class CheckWord(CheckWordBase):
    __tablename__ = "checkword"
    __table_args__ = {'extend_existing': True}
    user = Column(Integer,primary_key=True,nullable=False)
    check = Column(String(14),primary_key=True,nullable=False)
    updatetime = Column(Integer,primary_key=True,nullable=False)
    isused = Column(String(5),nullable=True)