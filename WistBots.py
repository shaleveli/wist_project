from WistAI import *
import Tree
import random


class MaxNAI(WistAI):
    data_type = None  # type: Tree.TreeData

    def __init__(self, game, player, dat=Tree.SimpleH):
        WistAI.__init__(self, game, player)
        self.data_type = dat

    def game_strategy(self, round_num):
        CARD_LOC = 1
        output = Tree.opt_card_h(round_num, self.data_type(self.game), self.player.idx)
        card = output[CARD_LOC]
        return card


class RandomAI(WistAI):

    def __init__(self, game, player):
        WistAI.__init__(self, game, player)

    def game_strategy(self):
        card_list = sorted(list(self.game.active_player().legal_play(self.game.lead_card)))
        rand = random.SystemRandom()
        return rand.choice(card_list)