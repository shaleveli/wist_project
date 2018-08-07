from Player import Player


class Game:
    active_players = None  # type: list[Player]
    players = None  # type: list[Player]

    def __init__(self, players_num, players_names=None):
        self.players_num = players_num
        self.players = []
        self.set_players(players_num, players_names)

    def turn(self):
        raise NotImplementedError("Game.turn() should be implemented")

    def set_players(self, players_num, players_names=None):
        raise NotImplementedError("Game.set_players() should be implemented")

    def __update_active_players(self):
        self.active_players = []
        for player in self.players:
            if player.turn:
                self.active_players.append(player)


