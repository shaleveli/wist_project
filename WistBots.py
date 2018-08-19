from WistAI import *
import Tree
import random
import Heuristics

class NormHAI(WistAI):
    def trump_bidding_strategy(self, *args):
        max_score = None
        cont = None
        for symbol in CardSymbol:
            cont_num = Heuristics.approx_rounds_simple(self.player.cards, symbol)
            score = self.game.contract_score(cont_num, cont_num)
            if max_score is None:
                max_score = score
                cont = WistContract(symbol, cont_num)
            elif score > max_score:
                max_score = score
                cont = WistContract(symbol, cont_num)
        if not self.game.trump_contract_legal(cont):
            return WistContract()
        else:
            return cont

    def contract_bidding_strategy(self, *args):
        cont = Heuristics.approx_rounds_simple(self.player.cards, self.game.trump_symbol)
        if cont not in self.game.legal_contracts():
            cont = cont + 1
        return cont

    def game_strategy(self, *args):
        raise NotImplementedError
    """ used in CONTRACT_BIDDING mode; returns the chosen card to drop"""

class MaxNAI(NormHAI):
    data_type = None  # type: Tree.TreeData
    round_num = None  # type: int
    version = None  # type: int

    def __init__(self, game, player, round_num, version, dat=Tree.SimpleH):
        WistAI.__init__(self, game, player)
        self.data_type = dat
        self.round_num =round_num
        self.version = version

    def game_strategy(self, *args):
        CARD_LOC = 1
        output = Tree.opt_card_h(self.round_num, self.data_type(self.game), self.player.idx)
        card = output[CARD_LOC]
        return card


class RandomAI(NormHAI):

    def __init__(self, game, player):
        WistAI.__init__(self, game, player)

    def game_strategy(self, *args):
        card_list = self.game.active_player().legal_play(self.game.lead_card)
        if len(card_list) == 0:
            print('bad')
        rand = random.SystemRandom()
        return rand.choice(card_list)