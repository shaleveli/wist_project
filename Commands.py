from Cmdl import *
from WistGame import *
from Globals import *


class ShowHandCards(Cmd):
    CMD_NAME = 'hand'

    def __init__(self):
        Cmd.__init__(self, self.CMD_NAME)

    def execute(self, wist_game, cmd_line):
        """gets cards of the player. need to implement __str__() of card and function like current player cards"""
        #card_num_to_string
        player_cards = wist_game.players[wist_game.active_player_idx].cards
        cards_strings = [card_to_str(card) for card in player_cards]
        cmd_line.print_array(cards_strings)


#done
class ShowBids(Cmd):
    CMD_NAME = 'bids'

    def __init__(self):
        Cmd.__init__(self, self.CMD_NAME)

    def execute(self, wist_game, cmd_line):
        """gets cards of the player. need to implement __str__() of contracts, and current player contracts"""
        contracts = [player.contract for player in wist_game.players]
        wins = [player.taken_rounds for player in wist_game.players]
        contracts = list(map(str, contracts))
        wins = list(map(str, wins))
        contract_strings = [str(i) + ')' + wins[i] + '/' + contracts[i] + ' 'for i in range(0, wist_game.PLAYERS_NUMBER)]
        cmd_line.print_array(contract_strings)


#done
class ShowWinCards(Cmd):
    CMD_NAME = 'pile'

    def __init__(self):
        Cmd.__init__(self, self.CMD_NAME)

    def execute(self, wist_game, cmd_line):
        """gets cards of the player. need to implement __str__() of card and function like current player cards"""
        cards_strings = list(map(card_to_str, wist_game.players[wist_game.active_player_idx].taken_cards_pack))
        cmd_line.print_array(cards_strings)
        cmd_line.print_console('\n')


#done
class ShowTable(Cmd):
    CMD_NAME = 'table'

    def __init__(self):
        Cmd.__init__(self, self.CMD_NAME)

    def execute(self, wist_game, cmd_line):
        """gets cards of the player. need to implement __str__() of card and function like wist table cards"""
        cards_strings = map(card_to_str, wist_game.current_round_cards).remove('None')
        cmd_line.print_array(cards_strings)
        cmd_line.print_console('\n')


#done
class MakeContractBid(Cmd):
    CMD_NAME = "bid"
    NUM_LOCATION = 0
    SYM_LOC = 1
    PASS_COMMAND = 'P'

    def __init__(self):
        Cmd.__init__(self, self.CMD_NAME)

    def execute(self, wist_game, cmd_line):
        if wist_game.game_mode == WistGameMode.GAME: #game mode
            raise ValueError("bid command cant be used in game mode")
        try:
            contract_num = int(self.cmd_args[self.NUM_LOCATION])
        except IndexError:
            raise TypeError("First argument must be an int or 'P'")
        except ValueError:
            if self.cmd_args[self.NUM_LOCATION] == self.PASS_COMMAND:
                return WistContract()
            else:
                raise TypeError("First argument must be an int or 'P'")
        if wist_game.game_mode == WistGameMode.TRUMP_BIDDING: #trump mode
            card_sym = None
            for sym in CardSymbol:
                try:
                    #print(card_symbol_to_string(sym))
                    if card_symbol_to_string(sym) == self.cmd_args[self.SYM_LOC]:
                        card_sym = sym
                except IndexError:
                    raise ValueError("Second argument must be a card symbol")
            if card_sym is None:
                raise ValueError("Second argument must be a card symbol")
            else:
                return WistContract(card_sym, contract_num)
        elif wist_game.game_mode == WistGameMode.CONTRACT_BIDDING: #contract mode
            return contract_num


#done
class DropCard(Cmd):
    def __init__(self):
        Cmd.__init__(self, self.CMD_NAME)
    CMD_NAME = "d"
    NUM_LOCATION = 0
    SYM_LOC = 1

    def execute(self, wist_game, cmd_line):
        if wist_game.game_mode == WistGameMode.GAME: #game mode
            pass
        else:
            raise ValueError("d command can be used only in game mode")
        try:
            card_num = int(self.cmd_args[self.NUM_LOCATION])
        except ValueError:
            raise TypeError("First argument[card_num] must be an int")

        card_sym = None
        for sym in CardSymbol:
            print(card_symbol_to_string(sym))
            if card_symbol_to_string(sym) == self.cmd_args[self.SYM_LOC]:
                card_sym = sym
        if card_sym is None:
            raise ValueError(self.cmd_args[self.SYM_LOC] + " is not a card symbol")
        else:
            return Card(card_num, card_sym)


class ShowTrump(Cmd):
    CMD_NAME = 'trump'
    def __init__(self):
        Cmd.__init__(self, self.CMD_NAME)

    def execute(self, wist_game, cmd_line):
        cmd_line.print_console(wist_game.trump_symbol)


class ShowTrumpTable(Cmd):
    CMD_NAME = 'trumpT'

    def __init__(self):
        Cmd.__init__(self, self.CMD_NAME)

    def execute(self, wist_game, cmd_line):
        for line in wist_game.trump_bidding_table:
            cmd_line.print_console(list(map(str, line)))


class ShowHelp(Cmd):
    CMD_NAME = 'help'

    def __init__(self):
        Cmd.__init__(self, self.CMD_NAME)

    def execute(self, wist_game, cmd_line):
        cmd_line.print_array([c.CMD_NAME for c in Cmd.__subclasses__()])


def card_to_str(card):
    return(card_num_to_string(card.num) + card_symbol_to_string(card.symbol))
