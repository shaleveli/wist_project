
from WistGame import WistGame
from Cmdl import CmdLine
from Commands import *
from TestAI import HumanAI

global wist_game
global cmdl
wist_game = WistGame()
cmdl = CmdLine(wist_game)
print("Init Variables")

test_str = ["bid 5 H", "bid P", "bid P", "bid P", "bid 5", "bid 5", "bid 5", "bid 5"]
AI = None
while 1:
    """if read_console returns somthing, pass in to game. catach game errors"""
    args = cmdl.read_console()
    if args is not None:
        try:
            wist_game.turn(args)
            AI = HumanAI(wist_game)
            if wist_game.game_mode == WistGameMode.GAME:
                print('wistP: ' + str(wist_game.active_player_idx))
                AI.card_prob_list()
        except ValueError as err:
            cmdl.print_console(err)
