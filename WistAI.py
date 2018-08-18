from Card import *
from WistGame import *
import copy
from WistPlayer import *


class WistAI:
    """the following are FUNCTIONS with a KnownInfo argument
    that return what the AI does in such a situation"""
    player = None  # type:WistPlayer
    game = None  # type:WistGame
    info = None  # type:KnownInfo

    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.info = player.known_info

    def output(self):
        "the only Public function of WistAI nevigates through its private functions"
        if self.game.game_mode == WistGameMode.TRUMP_BIDDING:

            return self.trump_bidding_strategy()
        elif self.game.game_mode == WistGameMode.CONTRACT_BIDDING:
            return self.contract_bidding_strategy()
        elif self.game.game_mode == WistGameMode.GAME:
            return self.game_strategy()

    def trump_bidding_strategy(self, *args):
        raise NotImplementedError
    """used in TRUMP_BIDDING mode; returns the suggested trump bidding contract"""

    def contract_bidding_strategy(self, *args):
        raise NotImplementedError
    """used in CONTRACT_BIDDING mode; returns the chosen final contract"""

    def game_strategy(self, *args):
        raise NotImplementedError
    """ used in CONTRACT_BIDDING mode; returns the chosen card to drop"""
