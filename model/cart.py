from __init__ import Base

from sqlalchemy import *


class Cart (Base):
    __tablename__ = "cart"
    ID_cart = Column(Integer, primary_key = True)
    user_id = Column(Integer,ForeignKey("users.ID_user", ondelete="CASCADE"))
    game_id = Column(Integer, ForeignKey("game.ID_game",ondelete="CASCADE"))
   