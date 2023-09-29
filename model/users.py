from __init__ import Base
from sqlalchemy import *


class User (Base):
    __tablename__ = "users"
    ID_user = Column(Integer, primary_key = True)
    ime = Column(String(50))
    prezime =Column(String(50))
    email = Column(String(50))
    password=Column(String(50))