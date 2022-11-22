from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DbHandler:
    def __init__(self,path,Base):
        self.engine = create_engine('sqlite:///'+path+"?check_same_thread=False")
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        Base.metadata.create_all(self.engine)