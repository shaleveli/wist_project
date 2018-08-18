
from Commands import *
from WistBots import *


wist_game = WistGame(False)
cmdl = CmdLine(wist_game)

# debugging CMD
test_str = ["bid 5 H", "bid P", "bid P", "bid P", "bid 5", "bid 5", "bid 5", "bid 5"]
#test_str = []
debug_idx = 0


while 1:
    """if read_console returns somthing, pass in to game. catach game errors"""
    if wist_game.game_mode == WistGameMode.END:
        print(wist_game.scores)
        break

    if debug_idx < len(test_str):
        args = cmdl.read_console(test_str[debug_idx])
        debug_idx = debug_idx + 1
    else:
        args = cmdl.read_console()

    if args is not None:
        try:
            wist_game.turn(args)
            if wist_game.game_mode == WistGameMode.GAME:
                pass
        except ValueError as err:
            cmdl.print_console(err)
