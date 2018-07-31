from Card import *
from WistGame import *


class KnownInfo:
    # Contains all the information that the AI player has about the current game.
    # This known information can be taken into account in the AI strategies.
    player_idx = None  # type: int
    cards = None  # type: [card]
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
    players_taken_cards = None  # type: [set(Card)]
    game_mode = None  # type: WistGameMode

    def __init__(self, game):  # initializes known information for the current active player
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
        self.player_idx = game.active_player_idx
        self.cards = list(game.players[self.player_idx].cards).sort
        self.game_mode = game.game_mode
        self.players_taken_cards = []
        self.players_contracts = []
        for i in range(0, self.PLAYERS_NUMBER):
            self.players_taken_cards.append(list(game.players[i].taken_cards_pack))
            self.players_contracts.append(game.players[i].contract)


class WistAI:

    """the following are FUNCTIONS with a KnownInfo argument
    that return what the AI does in such a situation"""
    known_info = None  # type:KnownInfo

    def __init__(self, game):
        self.known_info = KnownInfo(game)

    def output(self, game):
        "the only Public function of WistAI nevigates through its private functions"
        self.known_info.update(game)
        if self.known_info.game_mode == WistGameMode.TRUMP_BIDDING:
            self.__trump_bidding_strategy()
        elif self.known_info.game_mode == WistGameMode.CONTRACT_BIDDING:
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
