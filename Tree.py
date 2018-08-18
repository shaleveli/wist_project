from WistGame import *
from Card import *
import copy
import Heuristics
import random

class TreeData:
    """general type of tree, can be used in all trees with huristic"""
    # current game state
    game = None  # type:WistGame
    h = None
    last_dropped_card = None
    # list of all cards from original game
    card_list = None  # type:[Card]
    version = None  # type:int

    def __str__(self):
        ret = str(self.h) + ' ' + str(self.last_dropped_card)
        return ret

    def __init__(self, game, card=None, version=0):
        """1st init: insert the new modified game and a card.
            2nd init: insert last tree_dat Node the 1st game and a card
        """
        self.game = game
        self.last_dropped_card = card
        self.h = [None] * self.game.PLAYERS_NUMBER
        self.fill_h()
        self.version = version
        #print(self)

    def tree_top(self):
        return self.last_dropped_card is None

    def fill_h(self):
        for idx in range(self.game.PLAYERS_NUMBER):
            self.h[idx] = self.h_calc(idx)

    def h_calc(self, idx):
        raise NotImplementedError

    def has_children(self):
        if self.game.game_mode == WistGameMode.END:
            return False
        else:
            legal_player_cards = self.game.active_player().legal_play(self.game.lead_card)
            if len(legal_player_cards) > 0:
                return True
            else:
                return False

    def children_cards(self):
        legal_player_cards = self.game.active_player().legal_play(self.game.lead_card)
        return legal_player_cards

    def children_len(self):
        legal_player_cards = self.game.active_player().legal_play(self.game.lead_card)
        return len(legal_player_cards)

    def children(self):
        if self.version == 0:
            return self.children_v0()
        elif self.version == 1:
            return self.children_v1()

    # If cards are sorted its bad
    def children_v1(self):
        legal_player_cards = self.game.active_player().legal_play(self.game.lead_card)
        #random.shuffle(legal_player_cards)
        #legal_player_cards = self.sequences_pruning()
        for card in legal_player_cards:
            self.game.turn(card)
            yield self.__class__(self.game, card, self.version)
            self.game.reverse_regular_turn()

    def sequences_pruning(self):
        """ prun cards in sequences beacuse its actually the same"""
        legal_player_cards = self.game.active_player().legal_play(self.game.lead_card)
        legal_player_cards = sorted(legal_player_cards)
        idx = 0
        while idx < len(legal_player_cards) - 1:
            if self.game.similar_cards(legal_player_cards[idx], legal_player_cards[idx + 1]):
                #print('similar: ' + str(legal_player_cards[idx]) + str(legal_player_cards[idx + 1]))
                legal_player_cards.remove(legal_player_cards[idx])
            else:
                idx = idx + 1
        # random.shuffle(legal_player_cards)
        return legal_player_cards

    def children_v0(self):
        """return a list of all possible data that proceeds the game"""
        data_list = []
        if self.game.game_mode == WistGameMode.GAME:
            # legal cards but different instances then we need
            legal_player_cards = self.game.active_player().legal_play(self.game.lead_card)  # del sorted
            # for card in the legal current player cards
            for card in legal_player_cards:
                game_copy = copy.deepcopy(self.game)
                # same cards but different instances
                legal_player_cards_copy = game_copy.active_player().legal_play(game_copy.lead_card)
                # find the copy card that matches the original cards
                copy_card = card.card_in_list(legal_player_cards_copy)
                game_copy.turn(copy_card)
                data_list.append(self.__class__(game_copy, card, self.version))  # go to type of self
            return data_list
        elif self.game.game_mode == WistGameMode.END:
            pass

    def filtered_children(self):
        return self.children()


class ScoreH(TreeData):
    """specific TreeData that uses Score as Huristic"""
    min_h_val = None
    tot_h_sum = None

    def __init__(self, game, card=None, version=0):
        TreeData.__init__(self, game, card, version)

    def h_calc(self, idx, contract=None, *args):
        """option to add your contract"""
        player = self.game.players[idx]
        if contract is None:
            contract = player.contract
        approx_rounds = player.taken_rounds + self.approx_rounds(idx)
        return self.game.contract_score(contract, approx_rounds)

    def approx_rounds(self, idx):
        raise NotImplementedError


class SimpleH(ScoreH):
    """simple score huristic TreeData object. just counts the high cards in the hand"""
    def __init__(self, game, card=None, version=0):
        ScoreH.__init__(self, game, card, version)

    def approx_rounds(self, idx):
        cards = self.game.players[idx].cards
        trump_symbol = self.game.trump_symbol
        return Heuristics.approx_rounds_simple(cards, trump_symbol)


class NoH(ScoreH):
    def __init__(self, game, card=None, version=0):
        ScoreH.__init__(self, game, card, version)

    def approx_rounds(self, idx):
        return 0


# MaxN algorithm
def opt_card_h(max_round, data, player_idx):
    """gets 3 parameters: max_round the maximal rounds;
    data:input of type TreeData;
    player_idx the idx of the player that plays
    the functions return (leaf_huristic, last dropped card)
    """

    # if data is a leaf - END of the game
    if not data.has_children():
        tmp = data.h, data.last_dropped_card
        del data
        return tmp

    # if its the tree top and we have only one child
    if data.tree_top() and data.children_len() == 1:
        tmp = None, data.children_cards()[0]
        del data
        return tmp

    # if a round just ended - we now can calculate a new estimation of h
    if data.game.beginning_of_regular_turn() and not data.tree_top():
        max_round = max_round - 1

    # if we arrived max iterations we return the last h
    if max_round == 0:
        tmp = data.h[:], data.last_dropped_card
        del data
        return tmp

    # if the current play is done by our player - we can filter branches by prediction
    if data.game.active_player_idx == player_idx:
        children = data.filtered_children()
    # else we do nothing
    else:
        children = data.children()

    max_h = None
    max_last_card = None
    active_player_idx = data.game.active_player_idx
    # Cant use game inside here! its changing!!
    for child in children:
        #print(child)
        # calculate the child h
        h, last_card = opt_card_h(max_round, child, player_idx)
        if max_h is None:
            max_h = h
            max_last_card = child.last_dropped_card
            continue
        # if we found new h the maximize current player h
        if h[active_player_idx] > max_h[active_player_idx]:
            max_h = h
            max_last_card = child.last_dropped_card
    del children
    return max_h, max_last_card


def opt_card_h_shallow_pu(max_round, data, player_idx):
    """gets 3 parameters: max_round the maximal rounds;
    data:input of type TreeData;
    player_idx the idx of the player that plays
    the functions return (leaf_huristic, last dropped card)
    """
    # if data is a leaf - END of the game
    #print(data)
    if not data.has_children():
        tmp = data.h, data.last_dropped_card
        del data
        return tmp

    # if a round just ended - we now can calculate a new estimation of h
    if data.game.beginning_of_regular_turn() and not data.tree_top():
        max_round = max_round - 1

    # if we arrived max iterations we return the last h
    if max_round == 0:
        tmp = data.h[:], data.last_dropped_card
        del data
        return tmp

    # if the current play is done by our player - we can filter branches by prediction
    if data.game.active_player_idx == player_idx:
        children = data.filtered_children()
    # else we do nothing
    else:
        children = data.children()

    max_h = None
    max_last_card = None
    active_player_idx = data.game.active_player_idx
    # Cant use game inside here! its changing!!
    for child in children:
        # calculate the child h
        h, last_card = opt_card_h(max_round, child, player_idx)
        if max_h is None:
            max_h = h
            max_last_card = child.last_dropped_card
            continue
        # if we found new h the maximize current player h
        #print(str(h[active_player_idx]) + ' :>: ' + str(max_h[active_player_idx]))
        #print(h[active_player_idx] > max_h[active_player_idx])
        if h[active_player_idx] > max_h[active_player_idx]:
            max_h = h
            max_last_card = child.last_dropped_card
    del children
    return max_h, max_last_card



