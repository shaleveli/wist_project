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
    start_of_game = None  # type: bool
    trump_bidding_round = None  # type: int
    highest_bidding_contract = None  # type: WistContract
    trump_bidding_table = None  # type: [[WistContract]]
    # contains all trump-bidding contracts until now.
    # trump_bidding_table[i][j] is the contract of player j in the i+1 bidding round.
    bidding_winner = None  # type: int
    # the index of the player who won the bidding
    declared_contract = None  # type: bool
    # How many players declared their contract
    contracts_sum = None  # type: int
    is_under_game = None  # type: bool
    game_round = None  # type: int
    # During the bidding it is 0, and during the GAME mode it is the index of the current round
    current_round_cards = None  # type: [Card]
    lead_card = None  # type: Card
    takers_history = None  # type: [int]
    # takers_history[i] will contain the index of the taker of round i + 1
    winners = None  # type: [bool]
    # Starts as PLAYERS_NUMBER*[False], at the end contains whether each player won or not
    scores = None  # type: [int]
    # At the end of the game, contains the scores of each player
    ended_game = None  # type: bool

    def __init__(self):
        self.game_mode = WistGameMode.TRUMP_BIDDING
        Game.__init__(self, self.PLAYERS_NUMBER)
        self.active_player_idx = 0
        self.divide_cards()
        self.declared_contract = 0
        self.game_round = 0
        self.winners = self.PLAYERS_NUMBER * [False]
        self.scores = self.PLAYERS_NUMBER * [0]
        self.contracts_sum = 0
        self.ended_game = False
        self.start_of_game = True
        self.trump_bidding_round = 1
        self.trump_bidding_table = [[]]
        self.takers_history = []
        self.current_round_cards = self.PLAYERS_NUMBER * [None]

    def divide_cards(self):
        cards_pile = []
        for symbol in CardSymbol:
            for num in CardNum:
                if num != CardNum.JOKER:
                    cards_pile.append(Card(num, symbol))
        shuffle(cards_pile)
        for i in range(self.PLAYERS_NUMBER):
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
        for i in range(self.PLAYERS_NUMBER):
            if self.current_round_cards[i] is None:
                return False
        return True

    def beginning_of_regular_turn(self):
        for i in range(self.PLAYERS_NUMBER):
            if self.current_round_cards[i] is not None:
                return False
        return True

    def update_winners_and_scores(self):
        """Updates the lists winners and scores
        assuming the game was ended."""
        for i in range(self.PLAYERS_NUMBER):
            contract = self.players[i].contract
            if self.players[i].taken_rounds == contract:
                self.winners[i] = True
                if contract != 0:
                    self.scores[i] = 10 + contract*contract
                else:  # succeeded a contract of 0
                    if self.is_under_game:
                        self.scores[i] = 50
                    else:  # over game
                        self.scores[i] = 25
            else:
                self.winners[i] = False
                if contract != 0:
                    self.scores[i] = -10*abs(self.players[i].taken_rounds - contract)
                else:
                    self.scores[i] = -60 + 10*self.players[i].taken_rounds

    def trump_bidding_turn(self, bidding_contract):
        if self.game_mode != WistGameMode.TRUMP_BIDDING:
            raise ValueError("not in trump bidding mode")
        if self.start_of_game and bidding_contract.is_pass:
            raise ValueError("First player cannot pass")
        if not bidding_contract.is_pass:
            if self.trump_bidding_round != 1 and self.players[self.active_player_idx].passed:  # not supposed to happen
                raise ValueError("this player has already passed")
            if not self.start_of_game and bidding_contract <= self.highest_bidding_contract:
                raise ValueError("bidding_contract must be higher then highest_bidding")
        if self.start_of_game:
            self.start_of_game = False

        self.players[self.active_player_idx].passed = bidding_contract.is_pass
        self.trump_bidding_table[self.trump_bidding_round - 1].append(bidding_contract)
        if not bidding_contract.is_pass:
            self.highest_bidding_contract = bidding_contract
            self.bidding_winner = self.active_player_idx

        next_player = (self.active_player_idx + 1) % self.PLAYERS_NUMBER
        if self.end_of_trump_bidding() and next_player == self.bidding_winner:
            self.game_mode = WistGameMode.CONTRACT_BIDDING
            self.trump_symbol = self.highest_bidding_contract.symbol
        self.update_turn()
        if self.active_player_idx == 0:
            self.trump_bidding_table.append([])
            self.trump_bidding_round += 1
        # if the next player has already passed, automatically play his turn
        if self.players[next_player].passed:
            self.trump_bidding_turn(WistContract())

    def contract_bidding_turn(self, bidding_num):
        if self.game_mode != WistGameMode.CONTRACT_BIDDING:
            raise ValueError("not in contract bidding mode")
        if bidding_num not in self.legal_contracts():
            raise ValueError("Illegal contract")
        self.players[self.active_player_idx].contract = bidding_num
        self.declared_contract = self.declared_contract + 1
        self.contracts_sum = self.contracts_sum + bidding_num
        if self.end_of_contract_bidding():
            self.is_under_game = self.contracts_sum < self.CARDS_IN_HAND
            self.game_mode = WistGameMode.GAME
        self.update_turn()

    def legal_contracts(self):
        """returns a list of all legal bids for the next player"""
        legal_bids = []
        if self.declared_contract == 0:
            for i in range(self.highest_bidding_contract.num, self.CARDS_IN_HAND + 1):
                legal_bids.append(i)
        else:
            for i in range(self.CARDS_IN_HAND + 1):
                legal_bids.append(i)
            if (self.declared_contract == (self.PLAYERS_NUMBER - 1)
                    and (self.CARDS_IN_HAND - self.contracts_sum) in legal_bids):
                legal_bids.remove(self.CARDS_IN_HAND - self.contracts_sum)
        return legal_bids

    def regular_turn(self, card_from_hand):
        if self.game_mode != WistGameMode.GAME:
            raise ValueError("not in game mode")
        if self.beginning_of_regular_turn():
            self.lead_card = card_from_hand
            self.game_round = self.game_round + 1
        elif card_from_hand not in self.players[self.active_player_idx].legal_play(self.lead_card):
            raise ValueError("Card is not legal")
        self.players[self.active_player_idx].cards.remove(card_from_hand)
        self.current_round_cards[self.active_player_idx] = card_from_hand
        if self.end_of_regular_turn():
            win_player_idx = self.winning_player_in_round()
            self.takers_history.append(win_player_idx)
            self.players[win_player_idx].win_turn(set(self.current_round_cards))
            self.current_round_cards = self.PLAYERS_NUMBER*[None]
            self.lead_card = None
            if self.game_round == self.CARDS_IN_HAND:
                self.update_winners_and_scores()
                self.ended_game = True
            else:
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
                for i in range(players_num):
                    self.players.append(WistPlayer(players_names[i]))
        else:
            for i in range(players_num):
                self.players.append(WistPlayer())

    def compare_cards(self, card1, card2):
        """returns whether card1 is bigger than card2. The default is False"""
        if card1.symbol == card2.symbol:
            return card1.num.value > card2.num.value
        elif card1.symbol == self.trump_symbol:
            return True
        elif card2.symbol == self.trump_symbol:
            return False
        elif card1.symbol == self.lead_card.symbol:
            return True
        elif card2.symbol == self.lead_card.symbol:
            return False
        else:
            return False

    def winning_player_in_round(self):
        current_winner = 0
        for i in range(self.PLAYERS_NUMBER):
            if self.compare_cards(self.current_round_cards[i], self.current_round_cards[current_winner]):
                current_winner = i
        return current_winner

    def active_player_hand(self):
        return self.players[self.active_player_idx].cards


class WistGameMode(Enum):
    TRUMP_BIDDING = 1
    CONTRACT_BIDDING = 2
    GAME = 3


class WistContract:
    is_pass = None  # type: bool
    symbol = None  # type: CardSymbol
    num = None  # type: int

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

    def __le__(self, other):
        if self.num < other.num:
            return True
        elif self.num > other.num:
            return False
        elif self.symbol == other.symbol:
            return True
        elif self.symbol == CardSymbol.SPADE:
            return False
        elif self.symbol == CardSymbol.HEART:
            if other.symbol == CardSymbol.SPADE:
                return True
            else:
                return False
        elif self.symbol == CardSymbol.DIAMOND:
            if other.symbol == CardSymbol.SPADE or other.symbol == CardSymbol.HEART:
                return True
            else:
                return False
        else:  # self.symbol == CardSymbol.CLUB
            return True

    def __str__(self):
        if self.is_pass:
            return "<contract: PASS>"
        return "<contract: " + str(self.num) + " " + card_symbol_to_string(self.symbol) +">"

