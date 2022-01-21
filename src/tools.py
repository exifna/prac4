import time
from typing import List
from src.tables import Player, GameType
from src import crud
from threading import Thread
from time import sleep

class GameObj:
    def __init__(self, game_id : str, game_type: int):
        self.players : List[Player] = list()
        self.game_id : str = game_id
        self.last_step_time = time.time()
        self.game_type = game_type
        self.nowPlayer : Player = None
        self.month = 0
        self.level = 2
        self.end = False

        # -- действия -- #
        self.sales = False      # заявки на покупку сырья
        self.work  = False      # проиводство
        self.aviasales = False  # автосалон
        self.build = False      # заявки на строительство
        self.start = False      # началась ли игра
        self.z_sales = dict()   # заявки на покупку сырья: {'token' : {'count' : 1, 'amount' : 12}}

        # -- банк -- #
        self.bank_balance  = 0
        self.bank_material = 0
        self.bank_planes   = 0



    def addPlayes(self, player: Player):
        self.players.append(player)


    def startGame(self):
        crud.start_game(self.game_id)
        self.start = True
        self.run()

    def get_my_step(self, secret_token : str) -> str:

        if self.end:
            return 'end'

        elif not self.start:
            return 'start'

        if self.sales:
            return 'sales'

        elif self.work:
            return 'work'

        elif self.aviasales:
            return 'aviasales'

        elif self.build:
            return 'build'

        elif not self.nowPlayer:
            return 'wait'

        elif self.nowPlayer.secret_token == secret_token:
            return 'go'

        return 'wait'

    def run(self):
        Thread(target=self._run).start()

    def find_user(self, token : str) -> Player:
        for i in self.players:
            if i.secret_token == token:
                return i

    def _get_level_data(self):
        pass

    def _run(self):
        self.nowPlayer = self.players[0]
        while True:
            self.month += 1
            for player in self.players:
                self.last_step_time = time.time()
                self.nowPlayer = player

                while time.time() - self.last_step_time < 30:
                    sleep(0.1)


            if self.game_type == GameType.months and self.month == 12:
                self.end = True
                return

            for player in self.players:
                player.balance -= 300 * player.material
                player.balance -= 500 * player.flighters
                player.balance -= 1000 * player.workshops

            sleep(0.5)
