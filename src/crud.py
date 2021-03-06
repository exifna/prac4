from typing import Optional

import faker

from src.database import session
from src.tables import *



class LevelDataClass:
    level1: {
        'flighterBuyPrice': 1,

    }

def generatePlayer(game_id: str, nick: str, session = session) -> Player:
    token = faker.Faker().md5()
    player = Player(
        game_id = game_id,
        secret_token = token,
        nick = nick,
        balance = 10000,
        workshops = 2,
        flighters = 2,
        material = 4
    )
    session.add(player)
    return player

def changePlayerBalance(game_id:str, token: str, count: int, session = session):
    player = session.query(Player).filter(Player.game_id == game_id).filter(Player.secret_token == token).one()
    player.balance = count
    session.commit()

def get_player(game_id: str, token: str, session = session) -> Player:
    return session.query(Player).filter(Player.game_id == game_id).filter(Player.secret_token == token).one_or_none()


def get_level_data(level: int) ->

def but_flighter(game_id: str, token: str, session = session) -> Optional[bool]:
    player = get_player(game_id, token)
    if not player or player.flighters >= 6:
        return False

    if


def create_game(creator_nick: str, game_type: int, session = session) -> list:
    game_id = faker.Faker().md5()[:8]
    admin = generatePlayer(game_id, creator_nick)
    game = Game(
        creator_token = admin.secret_token,
        game_id = game_id,
        started = False,
        game_type = game_type
    )

    session.add(game)
    session.commit()
    return game, admin

def check_run_game(game_id: str, creator_token: str, session = session) -> bool:
    return bool(session.query(Game).filter(Game.game_id == game_id).filter(Game.creator_token == creator_token).filter(Game.started == False).one_or_none())

def accept_invite(game_id : str, nick: str, session = session) -> Player:
    if not session.query(Game).filter(Game.game_id == game_id).filter(Game.started == False).one_or_none():
        return None

    player = generatePlayer(game_id, nick)
    return player

def get_game_type_by_game_id(game_id : str, session = session):
    t = session.query(Game).filter(Game.game_id == game_id).one_or_none()
    if t:
        return t.game_type

    return None

def check_wait(game_id : str, session = session) -> bool:
    return bool(session.query(Game).filter(Game.game_id == game_id).filter(Game.started == False).one_or_none())

def start_game(game_id : str, session = session):
    session.query(Game).filter(Game.game_id == game_id).one().started = True
    session.commit()


