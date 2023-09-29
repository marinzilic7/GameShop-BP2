
from sqlalchemy.orm import relationship
from users import User
from games import Game
from category import Category
from cart import Cart
from shop import Shop
from __init__ import Base
from __init__  import engine


User.category = relationship('Category', back_populates='user')
User.game = relationship('Game', back_populates='user')
User.cart = relationship('Cart', back_populates='user')
Game.cart = relationship('Cart', back_populates="game")
Category.game = relationship('Game', back_populates="category")



Base.metadata.bind = engine
Base.metadata.create_all(bind=engine)