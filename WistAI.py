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
    #game_copy = None  # type:WistGame

    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.info = player.known_info
        #self.game_copy = copy.deepcopy(game)

    def output(self):
        "the only Public function of WistAI nevigates through its private functions"
        self.info = self.player.known_info
        if self.info.game_mode == WistGameMode.TRUMP_BIDDING:
            self.__trump_bidding_strategy()
        elif self.info.game_mode == WistGameMode.CONTRACT_BIDDING:
            self.__contract_bidding_strategy()
        else:
            self.__game_strategy()

    def __trump_bidding_strategy(self, *args):
        raise NotImplementedError
    """used in TRUMP_BIDDING mode; returns the suggested trump bidding contract"""

    def __contract_bidding_strategy(self, *args):
        raise NotImplementedError
    """used in CONTRACT_BIDDING mode; returns the chosen final contract"""

    def __game_strategy(self, *args):
        raise NotImplementedError
    """ used in CONTRACT_BIDDING mode; returns the chosen card to drop"""
