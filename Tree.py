from WistGame import *
from Card import *
import copy


class TreeData:
    """general type of tree, can be used in all trees with huristic"""
    # current game state
    game = None  # type:WistGame
    h = None
    last_dropped_card = None

    def __init__(self, game, card=None):
        self.game = game
        self.last_dropped_card = card
        self.h = [None] * self.game.PLAYERS_NUMBER
        self.fill_h()

    def fill_h(self):
        for idx in range(self.game.PLAYERS_NUMBER):
            self.h[idx] = self.h_calc(idx)

    def h_calc(self, idx):
        raise NotImplementedError

    def has_children(self):
        if self.game.game_mode == WistGameMode.END:
            return False
        else:
            legal_player_cards = sorted(list(self.game.active_player().legal_play(self.game.lead_card)))
            if len(legal_player_cards) > 0:
                return True
            else:
                return False

    def children(self):
        """return a list of all possible data that proceeds the game"""
        data_list = []
        if self.game.game_mode == WistGameMode.GAME:
            # legal cards but different instances then we need
            legal_player_cards = sorted(list(self.game.active_player().legal_play(self.game.lead_card)))

            # for card in the legal current player cards
            for card in legal_player_cards:
                game_copy = copy.deepcopy(self.game)
                # same cards but different instances
                legal_player_cards_copy = sorted(list(game_copy.active_player().legal_play(game_copy.lead_card)))
                # find the copy card that matches the original cards
                for c in legal_player_cards_copy:
                    if c.same(card):
                        copy_card = c
                game_copy.turn(copy_card)
                data_list.append(self.__class__(game_copy, card))  # go to type of self
        elif self.game.game_mode == WistGameMode.END:
            pass
        return data_list

    def filtered_children(self):
        return self.children()


class ScoreH(TreeData):
    """specific TreeData that uses Score as Huristic"""
    def __init__(self, game, card=None):
        TreeData.__init__(self, game, card)

    def h_calc(self, idx, *args):
        player = self.game.players[idx]
        approx_rounds = player.taken_rounds + self.approx_rounds(idx)
        return self.game.contract_score(player.contract, approx_rounds)

    def approx_rounds(self, idx):
        raise NotImplementedError


class SimpleH(ScoreH):
    """simple score huristic TreeData object. just counts the high cards in the hand"""
    def __init__(self, game, card=None):
        ScoreH.__init__(self, game, card)

    def approx_rounds(self, idx):
        cards = self.game.players[idx].cards
        rounds = 0
        for c in cards:
            if c.symbol == self.game.trump_symbol:
                if c.num.value > CardNum.TEN.value:
                    rounds = rounds + 1
            else:
                if c.num.value > CardNum.Q.value:
                    rounds = rounds + 1
        return rounds


# MaxN algorithm
def opt_card_h(max_round, data, player_idx):
    """gets 3 prameters: max_round the maximal rounds;
    data:input of type TreeData;
    player_idx the idx of the player that plays
    the functions return (leaf_huristic, last dropped card)
    """
    # if data is a leaf - END of the game
    if not data.has_children():
            return data.h, data.last_dropped_card

    # if a round just ended - we now can calculate a new estimation of h
    if data.game.beginning_of_regular_turn():
        max_round = max_round - 1

    # if we arrived max iterations
    if max_round == 0:
            return data.h, data.last_dropped_card

    # if the current play is done by our player - we can filter branches by prediction
    if data.game.active_player_idx == player_idx:
        children = data.filtered_children()
    # else we do nothing
    else:
        children = data.children()

    max_h = None
    max_last_card = None
    for child in children:
        # calculate the child h
        h, last_card = opt_card_h(max_round, child, player_idx)
        if max_h is None:
            max_h = h
            max_last_card = child.last_dropped_card
            continue
        # if we found new h the maximize current player h
        if h[data.game.active_player_idx] > max_h[data.game.active_player_idx]:
            max_h = h
            max_last_card = child.last_dropped_card
    return max_h, max_last_card

