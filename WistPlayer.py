from Player import Player
from Card import *
from WistGame import *


class WistPlayer(Player):
    contract = None  # type: int
    trump_contract = None  # type: WistContract
    passed = None  # type: bool
    taken_cards_pack = None  # type: set(Card)
    taken_rounds = None  # type: int
    known_info = None  # type: KnownInfo
    idx = None  # type: int

    def __init__(self, idx, name=None):
        Player.__init__(self, name)
        self.taken_rounds = 0
        self.taken_cards_pack = set()
        self.idx = idx

    def update(self, game):
        if self.known_info is None:
            self.known_info = KnownInfo(game, self.idx)
        else:
            self.known_info.update(game)

    def announced_contract(self):
        if self.contract is None:
            return False
        else:
            return True

    def legal_play(self, lead_card):
        """"returns a set of legal play cards.
        lead card is the 1st card in the round or NONE if the player is 1st"""
        if lead_card is None:
            return self.cards
        legal_cards = self.cards_in_symbol(lead_card.symbol)
        if len(legal_cards) == 0:
            legal_cards = self.cards
        return legal_cards

    def cards_in_symbol(self, symbol, cards=None):
        if cards is None:
            cards = self.cards
        card_set = set()
        for card in cards:
            if card.symbol == symbol:
                card_set.add(card)
        return card_set

    def win_turn(self, round_cards):
        self.taken_cards_pack = self.taken_cards_pack.union(round_cards)
        self.taken_rounds = self.taken_rounds + 1


class KnownInfo:
    # Contains all the information that the AI player has about the current game.
    # This known information can be taken into account in the AI strategies.
    active_player_idx = None  # type: int
    hand_cards = None  # type: [card]
    trump_symbol = None  # type: CardSymbol
    PLAYERS_NUMBER = 4
    CARDS_IN_HAND = 13
    trump_bidding_round = None
    highest_bidding_contract = None
    trump_bidding_table = None
    contracts_sum = None
    is_under_game = None  # type: bool
    game_round = None
    current_round_cards = None
    lead_card = None
    takers_history = None
    players_contracts = None  # type: [WistContract]
    players_taken_cards = None  # type: [[Card]]
    game_mode = None  # type: WistGameMode
    cards_pile = None  # type: [Card]
    unseen_cards = None  # type: [Card]
    seen_cards = None  # type: [Card]
    idx = None  # type: int
    player_symbol_list = None  # type: [{CardSymbol:bool}]
    #list of dictionary that stores if each player have specific symboll

    def __init__(self, game, idx):  # initializes known information for the current active player
        self.idx = idx
        self.player_symbol_list = self.PLAYERS_NUMBER * [None]
        for idx in range(self.PLAYERS_NUMBER):
            self.player_symbol_list[idx] = {}
            for sym in CardSymbol:
                self.player_symbol_list[idx][sym] = True
        self.update(game)

    def update(self, game):
        self.trump_symbol = game.trump_symbol
        self.PLAYERS_NUMBER = game.PLAYERS_NUMBER
        self.CARDS_IN_HAND = game.CARDS_IN_HAND
        self.trump_bidding_round = game.trump_bidding_round
        self.highest_bidding_contract = game.highest_bidding_contract
        self.trump_bidding_table = game.trump_bidding_table
        self.contracts_sum = game.contracts_sum
        self.is_under_game = game.is_under_game
        self.game_round = game.game_round
        self.current_round_cards = game.current_round_cards
        self.lead_card = game.lead_card
        self.takers_history = game.takers_history
        self.active_player_idx = game.active_player_idx  # change imdiatly!!
        self.hand_cards = sorted(list(game.players[self.idx].cards))
        self.game_mode = game.game_mode
        self.cards_pile = game.cards_pile
        self.players_taken_cards = []
        self.players_contracts = []
        self.seen_cards = self.hand_cards
        for i in range(0, self.PLAYERS_NUMBER):
            self.players_taken_cards.append(list(game.players[i].taken_cards_pack))
            self.players_contracts.append(game.players[i].contract)
            self.seen_cards = self.seen_cards + list(game.players[i].taken_cards_pack)
        self.unseen_cards = [c for c in self.cards_pile if c not in (self.seen_cards + self.current_round_cards)]
        # unseen cards are the cards that might be in the other players hands
        self.seen_cards = sorted(self.seen_cards)
        self.unseen_cards = sorted(self.unseen_cards)

        # Check if players dosent have a symbol
        if self.lead_card is not None:
            for idx in range(self.PLAYERS_NUMBER):
                if self.current_round_cards[idx] is not None:
                    if self.current_round_cards[idx].symbol != self.lead_card.symbol:
                        self.player_symbol_list[idx][self.lead_card.symbol] = False

