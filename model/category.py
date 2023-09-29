from __init__ import Base
from sqlalchemy import *


class Category (Base):
    __tablename__ = "category"
    ID_category = Column(Integer, primary_key = True)
    user_id = Column(Integer,ForeignKey("users.ID_user", ondelete="CASCADE"))
    ime = Column(String(50))
   