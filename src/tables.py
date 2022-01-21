from src.database import Base
from sqlalchemy import Column, String, Integer, Boolean


class Game(Base):
    __tablename__ = "games"
    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    creator_token = Column('creator_token', String)
    game_id = Column('game_id', String)
    started = Column('started', Boolean)
    game_type = Column('type', Integer)

class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    game_id = Column('game_id', String)
    secret_token = Column('token', String)
    nick = Column('nick', String)
    balance = Column('balance', String)
    workshops = Column('workshop', Integer)
    flighters = Column('flighter', Integer)
    material = Column('material', Integer)





class GameType:
    months = 0
    winner = 1
