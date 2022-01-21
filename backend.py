import time
from typing import Dict
from flask_cors import CORS
from flask import Flask, jsonify, request
from src import crud
from src.tools import GameObj

app = Flask(__name__)
CORS(app)
games : Dict[str, GameObj] = dict()

@app.post("/create_game")
def create_game():
    global games
    data = request.json
    nick = data['nick']
    game_type = data['game_type']
    game, admin = crud.create_game(nick, game_type)
    game_obj = GameObj(game.game_id, game_type)
    games[game.game_id] = game_obj
    game_obj.addPlayes(admin)
    return jsonify({
        'game_id' : game.game_id,
        'secret_token' : game.creator_token
    })

@app.post('/accept_invite')
def accept_invite():
    global games
    data = request.json
    game_id = data['game_id']
    nick = data['nick']
    player = crud.accept_invite(game_id, nick)
    if not player:
        return jsonify({
            'success' : False
        })
    games[game_id].addPlayes(player)
    return jsonify({
        'success' : True,
        'game_id': player.game_id,
        'secret_token' : player.secret_token,
        'nick': player.nick
    })



@app.post(f'/run_game')
def run_game():
    data = request.json
    game_id = data['game_id']
    token = data['token']
    if not crud.check_run_game(game_id, token):
        return jsonify({'success': False})
    global games
    game = games[game_id]
    game.startGame()

    return jsonify({'success' : True})

@app.post("/check_run")
def check_run():
    token = request.json['token']
    game_id = request.json['game_id']
    return {'run_button': crud.check_run_game(game_id, token),
            'wait': crud.check_wait(game_id)}

@app.post("/game")
def get_level():
    global games
    return jsonify({
        'level' : games[request.json['game_id']].level,
        'month' : games[request.json['game_id']].month
    })

@app.post('/me')
def get_me():
    global games
    data = request.json
    token = data["token"]
    game_id = data["game_id"]
    player = games[game_id].find_user(token)
    if not player:
        return jsonify(success = False)

    result = {
        'balance' : player.balance,
        'workshops' : player.workshops,
        'flighters' : player.flighters,
        'material' : player.material,
        'success': True
    }
    return jsonify(result)

@app.post('/get_event')
def get_player_event():
    global games
    game_id = request.json['game_id']
    token = request.json['token']
    game = games[game_id]
    data = game.get_my_step(token)
    temp_time = None
    if data in ["go", "sales", "work", "aviasales", "build"]:
        temp_time = 30 - int(time.time() - game.last_step_time)
    return jsonify({'step' : data, 'seconds' : temp_time or 30})

@app.post('/game_type')
def get_game_type():
    game = crud.get_game_type_by_game_id(request.json["game_id"])
    return jsonify(
         'не удалось получить' if game == None else 'ограниченное время - 12 месяцев' if game == 0 else 'единственный победитель'
    )

@app.post('/players')
def get_players():
    global games
    game_id = request.json['game_id']
    return jsonify([x.nick for x in games[game_id].players])



app.run("0.0.0.0", 12001)
