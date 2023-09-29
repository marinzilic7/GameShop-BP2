from __init__ import Base

from sqlalchemy import *


class Game (Base):
    __tablename__ = "game"
    ID_game = Column(Integer, primary_key = True)
    user_id = Column(Integer,ForeignKey("users.ID_user", ondelete="CASCADE"))
    category_id = Column(Integer,ForeignKey("category.ID_category", ondelete="CASCADE"))
    ime = Column(String(50))
    opis =Column(String(200))
    cijena=Column(Integer)
  