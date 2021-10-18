from sqlalchemy import create_engine,func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column,Integer,String,TEXT
from nonebot import get_driver

from .config import Config
conf = get_driver().config

db = conf.root+"bot.db"
engine = create_engine("sqlite:///"+db,echo=False)
Base = declarative_base()

class Allsettings(Base):
    __tablename__ = "bot_disabled_settings"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer,primary_key=True)
    Pluginname = Column(TEXT)
    Groupid = Column(TEXT)

def init():
    Base.metadata.create_all(engine, checkfirst=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def push(session,dic):
    add = []
    for k,v in dic.items():
        for m in v:
            if session.query(func.count("*")).select_from(Allsettings).filter(Allsettings.Pluginname==k).filter(Allsettings.Groupid==m).scalar() ==0:
                add.append(Allsettings(Pluginname=k,Groupid=m))
    session.add_all(add)
    session.commit()

def fetch(session):
    dic = {}
    a = session.query(Allsettings).all()
    for i in a:
        try:
            dic[i.Pluginname].append(i.Groupid)
        except KeyError:
            dic[i.Pluginname] = [i.Groupid]
    conf.disabled_settings = dic
    
def pushone(session,tupl):
    if session.query(func.count("*")).select_from(Allsettings).filter(Allsettings.Pluginname==tupl[0]).filter(Allsettings.Groupid==tupl[1]).scalar() ==0:
        session.add(Allsettings(Pluginname=tupl[0],Groupid=tupl[1]))
        session.commit()
        return True
    else:
        return False

def pullone(session,tupl):
    if session.query(func.count("*")).select_from(Allsettings).filter(Allsettings.Pluginname==tupl[0]).filter(Allsettings.Groupid==tupl[1]).scalar() ==0:
        return False
    else:
        todel = session.query(Allsettings).filter(Allsettings.Pluginname==tupl[0]).filter(Allsettings.Groupid==tupl[1]).first()
        session.delete(todel)
        session.commit()
        return True