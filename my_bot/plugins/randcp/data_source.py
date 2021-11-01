from sqlalchemy import create_engine,func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column,Integer,String,TEXT
import os.path
db_=os.path.split(os.path.realpath(__file__))[0]+"/cptimes.db?check_same_thread=False",
engine = create_engine("sqlite:///"+db_[0],echo=False)
Base = declarative_base()

def get_table(table_name):
    '''对不同群生成独立的数据库表 参数:表名 返回：orm对象'''
    class keywords(Base):
        __tablename__ = table_name
        __table_args__ = {'extend_existing': True}
        USER_ID = Column(Integer,primary_key=True)
        REQUESTTIMES = Column(Integer)
        UPDATETIME = Column(TEXT)
    return keywords

def init_table(lis_):
    '''初始化table 参数:群列表 返回：对象字典'''
    returnlis = {}
    for i in lis_:
        returnlis[i] = get_table(i)
    Base.metadata.create_all(engine, checkfirst=True)
    return returnlis

def init(lis_):
    '''初始化数据库 参数:群列表 返回：数据库操作接口，对象字典'''
    dic = init_table(lis_)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session,dic

def check_can(session,group_orm,user_id,updatetime):
    m = session.query(group_orm).filter(group_orm.USER_ID==user_id).first()
    if m == None:
        session.add(group_orm(USER_ID=user_id,REQUESTTIMES=1,UPDATETIME=updatetime))
        session.commit()
        return True
    elif m.UPDATETIME==updatetime and m.REQUESTTIMES < 5:
        m.REQUESTTIMES+=1
        session.commit()
        return True
    elif m.UPDATETIME!=updatetime:
        m.UPDATETIME=updatetime
        m.REQUESTTIMES=1
        session.commit()
        return True
    elif m.UPDATETIME==updatetime and m.REQUESTTIMES >= 5:
        return False
