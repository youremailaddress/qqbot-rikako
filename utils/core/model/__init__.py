from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from sqlalchemy import Column, Integer, String,ForeignKey,UniqueConstraint
from sqlalchemy.orm import relationship,backref
from .confmodel import Personalize
from .funcmodel import Func
from .permmodel import Func_User,Disable
from .timermodel import Time

