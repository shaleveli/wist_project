from WistGame import *
from Card import *
import copy
import Heuristics
import random


class CardsTreeData:
    """ data structure to pass cards for the next turn for next nodes.
        DO NOT EDIT this object outside this instance
    """
    first_player_idx = None  # type:int

    players_children_cards = None  # type:[[card]]
    game = None  # type:WistGame

    one_player_data_flag = None  # type:bool

    def __init__(self, game, player_idx=None):
        """can isert player idx, and this function will calculate only his card"""
        self.game = game
        LAST_PLAYER = 1
        self.first_player_idx = self.game.player_turn(LAST_PLAYER)
        self.players_children_cards = self.game.PLAYERS_NUMBER * [None]
        if player_idx is not None:
            self.one_player_data_flag = True
        else:
            self.one_player_data_flag = False
        self.fill(player_idx)

    def fill(self, player_idx=None):
        if player_idx is None:
            for idx in range(self.game.PLAYERS_NUMBER):
                if idx != self.first_player_idx:
                    self.players_children_cards[idx] = self.game.players[idx].legal_play(self.game.lead_card)
                    self.players_children_cards[idx] = self.sequences_pruning(self.players_children_cards[idx])
                else:
                    self.players_children_cards[idx] = self.game.players[idx].legal_play()
                    self.players_children_cards[idx] = self.sequences_pruning(self.players_children_cards[idx])
        else:
            idx = player_idx
            self.players_children_cards[idx] = self.game.players[idx].legal_play(self.game.lead_card)
            self.players_children_cards[idx] = self.sequences_pruning(self.players_children_cards[idx])

    def children_cards(self, player_idx):
        return self.players_children_cards[player_idx]

    def sequences_pruning(self, cards):
        """modifies cards substracts double cards"""
        legal_player_cards = sorted(cards)
        idx = 0
        while idx < len(legal_player_cards) - 1:
            if self.game.similar_cards(legal_player_cards[idx], legal_player_cards[idx + 1]):
                legal_player_cards.remove(legal_player_cards[idx])
            else:
                idx = idx + 1
        random.shuffle(legal_player_cards)
        return legal_player_cards

    def is_valid(self):
        if self.game.beginning_of_regular_turn() or self.one_player_data_flag:
            return False
        else:
            return True


class TreeData:
    """general type of tree, can be used in all trees with huristic"""
    # current game state
    game = None  # type:WistGame
    h = None
    last_dropped_card = None
    version = None  # type:int
    children_cards = None  # type:[Card]
    cards_data = None  # type: CardsTreeData
    # for each player contains its

    def __str__(self):
        ret = str(self.h) + ' ' + str(self.last_dropped_card)
        return ret

    def __init__(self, game, card=None, version=1, cards_data=None):
        """ card: if None its the top of the tree, else its son of another node
            cards data: if None its the player that just starting the turn, and it will create another cards_data
            else it need to pass it on
        """
        self.game = game
        self.last_dropped_card = card
        self.h = [None] * self.game.PLAYERS_NUMBER
        self.fill_h()
        self.version = version
        if cards_data is not None and cards_data.is_valid():
            self.cards_data = cards_data
            self.children_cards = cards_data.children_cards(game.active_player_idx)
        else:
            self.cards_data = CardsTreeData(self.game, self.game.active_player_idx)
            self.children_cards = self.cards_data.children_cards(self.game.active_player_idx)

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
            if self.children_len() > 0:
                return True
            else:
                return False

    def children_len(self):
        return len(self.get_children_cards())

    def children(self):
        if self.version == 0:
            return self.children_v0()
        elif self.version == 1:
            return self.children_v1()

    def set_children_cards(self):
        self.children_cards = self.game.active_player().legal_play(self.game.lead_card)
        self.children_cards = self.sequences_pruning(self.children_cards)

    def get_children_cards(self):
        if self.children_cards is None:
            # cod is problamatic. fix it
            print('prob')
            self.set_children_cards()
        #return self.game.active_player().legal_play(self.game.lead_card)
        return self.children_cards

    # maybe will use in the future
    def children_v1(self):
        legal_player_cards = self.get_children_cards()
        for card in legal_player_cards:
            self.game.turn(card)
            yield self.__class__(self.game, card, self.version)
            self.game.reverse_regular_turn()

    def get_child(self, card):
        """ create the node that created from a card. if its begginng of round create new card data
            Speed modification implemented here
        """
        if not self.cards_data.is_valid():
            self.game.turn(card)
            return self.__class__(self.game, card, self.version, CardsTreeData(self.game))
        else:
            self.game.turn(card)
            return self.__class__(self.game, card, self.version, self.cards_data)

    def pop_child(self):
        self.game.reverse_regular_turn()

    def filtered_children(self):
        return self.children()

    """
    def sequences_pruning(self, cards):
        legal_player_cards = sorted(cards)
        idx = 0
        while idx < len(legal_player_cards) - 1:
            if self.game.similar_cards(legal_player_cards[idx], legal_player_cards[idx + 1]):
                legal_player_cards.remove(legal_player_cards[idx])
            else:
                idx = idx + 1
        random.shuffle(legal_player_cards)
        return legal_player_cards
    
    # Old Function
    def children_v0(self):
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
    """


class ScoreH(TreeData):
    """specific TreeData that uses Score as Huristic"""
    min_h_val = None
    tot_h_sum = None

    def __init__(self, game, card=None, version=1, cards_data=None):
        TreeData.__init__(self, game, card, version, cards_data)

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

    def __init__(self, game, card=None, version=1, cards_data=None):
        ScoreH.__init__(self, game, card, version, cards_data)

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
        tmp = None, data.get_children_cards()[0]
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
    """
    # if the current play is done by our player - we can filter branches by prediction
    if data.game.active_player_idx == player_idx:
        children = data.filtered_children()
    # else we do nothing
    else:
        children = data.children()
    """
    max_h = None
    max_last_card = None
    active_player_idx = data.game.active_player_idx
    cards_list = data.get_children_cards()[:]
    # Cant use game inside here! its changing!!
    for card in cards_list:
        child = data.get_child(card)
        # calculate the child h
        h, last_card = opt_card_h(max_round, child, player_idx)
        data.pop_child()
        if max_h is None:
            max_h = h
            max_last_card = child.last_dropped_card
            continue
        # if we found new h the maximize current player h
        if h[active_player_idx] > max_h[active_player_idx]:
            max_h = h
            max_last_card = child.last_dropped_card
    return max_h, max_last_card

