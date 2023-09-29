from __init__ import Base
from sqlalchemy import *


class Shop (Base):
    __tablename__ = "shop"
    ID_shop = Column(Integer, primary_key = True)
    ime = Column(String(50))
    adresa =Column(String(50))
    kontakt = Column(Integer)