
from WistGame import WistGame
from Cmdl import CmdLine
from Commands import *
from TestAI import HumanAI
from WistBots import *

wist_game = WistGame(False)
cmdl = CmdLine(wist_game)

# debugging CMD
test_str = ["bid 5 H", "bid P", "bid P", "bid P", "bid 5", "bid 5", "bid 5", "bid 5"]
debug_idx = 0


while 1:
    """if read_console returns somthing, pass in to game. catach game errors"""
    if debug_idx < len(test_str):
        args = cmdl.read_console(test_str[debug_idx])
        debug_idx = debug_idx + 1
    else:
        args = cmdl.read_console()
    if args is not None:
        try:
            wist_game.turn(args)
            AI = HumanAI(wist_game)
            if wist_game.game_mode == WistGameMode.GAME:
                print('wistP: ' + str(wist_game.active_player_idx))
                MAX_ROUNDS = 2
                # calculates which card to put for each player

                # MAXN AI
                a = MaxNAI(wist_game, wist_game.active_player()).game_strategy(MAX_ROUNDS)
                # Random AI
                b = RandomAI(wist_game, wist_game.active_player()).game_strategy()
                print(a)
                print(b)

        except ValueError as err:
            cmdl.print_console(err)
