from Card import *
from WistGame import *


class KnownInfo:
    # Contains all the information that the AI player has about the current game.
    # This known information can be taken into account in the AI strategies.
    player_idx = None
    cards = None
    trump_symbol = None
    PLAYERS_NUMBER = 4
    CARDS_IN_HAND = 13
    trump_bidding_round = None
    highest_bidding_contract = None
    trump_bidding_table = None
    contracts_sum = None
    is_under_game = None
    game_round = None
    current_round_cards = None
    lead_card = None
    takers_history = None
    players_contracts = None

    def __init__(self, game):  # initializes known information for the current active player
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
        self.cards = game.players[self.player_idx].cards


class WistAI:
    # the following are FUNCTIONS with a KnownInfo argument
    # that return what the AI does in such a situation
    trump_bidding_strategy = None  # used in TRUMP_BIDDING mode; returns the suggested trump bidding contract
    contract_bidding_strategy = None  # used in CONTRACT_BIDDING mode; returns the chosen final contract
    game_strategy = None  # used in CONTRACT_BIDDING mode; returns the chosen card to drop
