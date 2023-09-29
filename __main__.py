from model import *
from model.relacije import *
from model.cache import region, api


ID = 2
KEY = f'id_food{ID}'
pero = region.get(KEY)
print(pero)
if pero is api.NO_VALUE:
    pero = Session.query(Game).filter(Game.ID_game==ID).one()
    region.set(KEY, pero)
