
from WistGame import WistGame
from Cmdl import CmdLine
from Commands import *
global wist_game
global cmdl
wist_game = WistGame()
cmdl = CmdLine(wist_game)
print("Init Variables")

test_str = ["bid 5 H", "bid P", "bid P", "bid P", "bid 5", "bid 5", "bid 5", "bid 5"]
while 1:
    """if read_console returns somthing, pass in to game. catach game errors"""
    args = cmdl.read_console()
    if args is not None:
        try:
            wist_game.turn(args)
        except ValueError as err:
            cmdl.print_console(err)
