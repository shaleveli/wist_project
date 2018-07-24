from Player import Player
from Card import *
from WistGame import *


class WistPlayer(Player):
    contract = None  # type:int
    trump_contract = None  # type:WistContract
    passed = None  # type:bool
    taken_cards_pack = None  # type:set(Card)
    wined_rounds = None  # type:int

    def __init__(self, name=None):
        Player.__init__(name)
        self.wined_rounds = 0
        self.taken_cards_pack = set()
        pass

    def announced_contract(self):
        if self.contract is None:
            return False
        else:
            return True

    def legal_play(self, lead_card):
        """"returns set of legal play cards. lead card is the 1st card in the round or NONE if the player is 1st"""
        legal_cards = self.cards_in_symbol(lead_card.symbol)
        if len(legal_cards) == 0:
            legal_cards = self.cards
        return legal_cards

    def cards_in_symbol(self, symbol):
        card_set = set()
        for card in self.cards:
            if card.symbol == symbol:
                card_set.add(card)
        return card_set

    def win_turn(self, round_cards):
        self.taken_cards_pack = self.taken_cards_pack.union(round_cards)
        self.wined_rounds = self.wined_rounds + 1