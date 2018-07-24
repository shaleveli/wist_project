from Game import Game
from Card import *
from WistPlayer import WistPlayer
from random import shuffle


class WistGame(Game):
    game_mode = None  # type: WistGameMode
    trump_symbol = None  # type: Symbol
    PLAYERS_NUMBER = 4
    CARDS_IN_HAND = 13
    active_player_idx = None  # type: int
    highest_bidding_contract = None  # type: WistContract
    current_round_cards = PLAYERS_NUMBER*[None]  # type: list[Card]
    lead_card = None  # type: Card
    first_contract = None # type: bool

    def __init__(self):
        self.game_mode = WistGameMode.TRUMP_BIDDING
        Game.__init__(self, self.PLAYERS_NUMBER)
        self.active_player_idx = 0
        self.divide_cards()
        self.first_contract = False

    def divide_cards(self):
        cards_pile = []
        for symbol in all_card_symbols():
            for num in all_card_nums():
                cards_pile.append(Card(num, symbol))
        shuffle(cards_pile)
        for i in xrange(self.PLAYERS_NUMBER):
            self.players[i].set_cards(set(cards_pile[i*self.CARDS_IN_HAND:(i+1)*self.CARDS_IN_HAND]))

    def end_of_trump_bidding(self):
        cnt_passed = 0
        for player in self.players:
            if player.passed:
                cnt_passed = cnt_passed + 1
        if cnt_passed < self.PLAYERS_NUMBER - 1:
            return False
        else:
            return True

    def end_of_contract_bidding(self):
        cnt = 0
        for player in self.players:
            if player.announced_contract():
                cnt = cnt + 1
        if cnt == self.PLAYERS_NUMBER:
            return True
        else:
            return False

    def end_of_regular_turn(self):
        for i in xrange(self.PLAYERS_NUMBER):
            if self.current_round_cards is None:
                return False
        return True

    def beginning_of_regular_turn(self):
        for i in xrange(self.PLAYERS_NUMBER):
            if self.current_round_cards is not None:
                return False
        return True

    def winning_players(self):
        """If the game was ended, returns a list that determines whether each player won.
        Otherwise, returns None"""


    def trump_bidding_turn(self, bidding_contract):
        if not self.players[self.active_player_idx].passed:
            if bidding_contract.is_pass:
                self.players[self.active_player_idx].passed = True
            else:
                self.players[self.active_player_idx].passed = False
                if bidding_contract <= self.highest_bidding_contract:
                    raise ValueError("bidding_contract must be higher then highest_bidding_contract")
                else:
                    self.highest_bidding_contract = bidding_contract
        if self.end_of_trump_bidding():
            self.game_mode = WistGameMode.CONTRACT_BIDDING
            self.trump_symbol = self.highest_bidding_contract.symbol
            self.first_contract = True
        self.update_turn()

    def contract_bidding_turn(self, bidding_num):
        if self.first_contract and bidding_num < self.highest_bidding_contract.num:
            raise ValueError("Contract must be at least as stated")
        self.players[self.active_player_idx].contract = bidding_num
        self.first_contract = False
        if self.end_of_contract_bidding():
            self.game_mode = WistGameMode.GAME
        self.update_turn()

    def regular_turn(self, card_from_hand):
        if self.beginning_of_regular_turn():
            self.lead_card = card_from_hand
        elif card_from_hand not in self.players[self.active_player_idx].legal_play():
            raise ValueError("Card is not legal")
        self.players[self.active_player_idx].cards.remove(card_from_hand)
        self.current_round_cards[self.active_player_idx] = card_from_hand
        if self.end_of_regular_turn():
            win_player_idx = self.winning_player_in_round()
            self.players[win_player_idx].win_turn(set(self.current_round_cards))
            self.current_round_cards = self.PLAYERS_NUMBER*[None]
            self.update_turn(win_player_idx)
            return
        self.update_turn()

    def turn(self, *args):
        if self.game_mode == WistGameMode.TRUMP_BIDDING:
            self.trump_bidding_turn(*args)
        elif self.game_mode == WistGameMode.CONTRACT_BIDDING:
            self.contract_bidding_turn(*args)
        elif self.game_mode == WistGameMode.GAME:
            self.regular_turn(*args)

    def update_turn(self, player_idx=None):
        self.players[self.active_player_idx].turn = False
        if player_idx is None:
            self.active_player_idx = (self.active_player_idx + 1) % self.PLAYERS_NUMBER
        else:
            self.active_player_idx = player_idx
        self.active_players = [self.players[self.active_player_idx]]
        self.players[self.active_player_idx].turn = True

    def set_players(self, players_num, players_names=None):
        if players_names is not None:
            if len(players_names) != players_num:
                raise ValueError("players_names length must be players_num")
            else:
                for i in xrange(players_num):
                    self.players.append(WistPlayer(players_names[i]))
        else:
            for i in xrange(players_num):
                self.players.append(WistPlayer())

    def compare_cards(self, card1, card2, lead_symbol):
        """returns whether card1 is bigger than card2. The default is False"""
        if card1.symbol == card2.symbol:
            return card1.num < card2.num
        elif card1.symbol == self.trump_symbol:
            return True
        elif card2.symbol == self.trump_symbol:
            return False
        elif card1.symbol == lead_symbol:
            return True
        elif card2.symbol == lead_symbol:
            return False
        else:
            return False

    def winning_player_in_round(self):
        current_winner = 0
        for i in xrange(self.PLAYERS_NUMBER):
            if self.current_round_cards[i] > self.current_round_cards[current_winner]:
                current_winner = i
        return current_winner


class WistGameMode(Enum):
    TRUMP_BIDDING = 1
    CONTRACT_BIDDING = 2
    GAME = 3


class WistContract:
    is_pass = None  #type: bool
    symbol = None  #type: CardSymbol
    num = None  #type: int

    def __init__(self, symbol=None, num=None):
        if symbol is None and num is None:
            self.is_pass = True
            self.symbol = None
            self.num = None
        elif not (not (symbol is None) and not (num is None)):
            raise ValueError("Exactly one None argument is not allowed")
        else:
            self.is_pass = False
            self.symbol = symbol
            self.num = num

    def __cmp__(self, other):
        if self.num < other.num:
            return -1
        elif self.num > other.num:
            return 1
        elif self.symbol == other.symbol:
            return 0
        elif self.symbol == CardSymbol.SPADE:
            return 1
        elif self.symbol == CardSymbol.HEART:
            if other.symbol == CardSymbol.SPADE:
                return -1
            else:
                return 1
        elif self.symbol == CardSymbol.DIAMOND:
            if other.symbol == CardSymbol.SPADE or other.symbol == CardSymbol.HEART:
                return -1
            else:
                return 1
        else:  # self.symbol == CardSymbol.CLUB
            return -1

