from sqlalchemy import create_engine,func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column,Integer,String,TEXT
import os.path
db_=os.path.split(os.path.realpath(__file__))[0]+"/keyword.db?check_same_thread=False",
engine = create_engine("sqlite:///"+db_[0],echo=False)
Base = declarative_base()

def get_table(table_name):
    '''对不同群生成独立的数据库表 参数:表名 返回：orm对象'''
    class keywords(Base):
        __tablename__ = table_name
        __table_args__ = {'extend_existing': True}
        id = Column(Integer,primary_key=True)
        KEYWORD = Column(TEXT)
        RESPONSE = Column(TEXT)
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

def pushwords(session,group_orm,keyword,response):
    if not keyword or not response:
        return False
    if session.query(func.count("*")).select_from(group_orm).filter(group_orm.KEYWORD==keyword).filter(group_orm.RESPONSE==response).scalar() ==0:
        session.add(group_orm(KEYWORD=keyword,RESPONSE=response))
        session.commit()
        return True
    else:
        return False

def delkeywords(session,group_orm,keyword,response):
    if not keyword or not response:
        return False
    if session.query(func.count("*")).select_from(group_orm).filter(group_orm.KEYWORD==keyword).filter(group_orm.RESPONSE==response).scalar() ==0:
        return False
    todel = session.query(group_orm).filter(group_orm.KEYWORD==keyword).filter(group_orm.RESPONSE==response).first()
    session.delete(todel)
    session.commit()
    return True
        
def get_random_reply(session,group_orm,keyword):
    try:
        return session.query(group_orm).filter(group_orm.KEYWORD==keyword).order_by(func.random()).first().RESPONSE
    except:
        return None

def get_keyword_list(session,group_orm):
    return [i[0] for i in session.query(group_orm.KEYWORD.distinct()).all()]

def get_keyword_response_form(session,group_orm):
    keyword_list = get_keyword_list(session, group_orm)
    dic = {}
    for i in keyword_list:
        dic[i] = [i[0] for i in session.query(group_orm.RESPONSE).filter(group_orm.KEYWORD==i).all()]
    return dic


