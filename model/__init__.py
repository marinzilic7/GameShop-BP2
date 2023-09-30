from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

""" engine = create_engine("mysql+pymysql://root@localhost:3306/gameshop") """


engine = create_engine("mysql+pymysql://gameshop:gameshop123@mysql:3306/gameshop") 
Session = sessionmaker(bind=engine)

Session = Session()

Base = declarative_base()