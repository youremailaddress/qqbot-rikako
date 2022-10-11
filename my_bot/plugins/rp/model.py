from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.orm import relationship,backref
RPBase = declarative_base()

class RP(RPBase):
    __tablename__ = "rp"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True,nullable=False)
    rp = Column(Integer,nullable=False)
    comment = Column(String(144),nullable=False)
    updatetime = Column(String(64),nullable=False)