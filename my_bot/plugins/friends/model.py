from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.orm import relationship,backref
FriendBase = declarative_base()

class FRI(FriendBase):
    __tablename__ = "friend"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True,nullable=False)
    updatetime = Column(String(64),nullable=False)