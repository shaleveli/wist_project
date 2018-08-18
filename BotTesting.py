from WistGame import *
from WistBots import *
import cProfile


def bot_game(bots, game, debug=False):
    while 1:
        if game.game_mode == WistGameMode.END:
            return game.scores

        args = bots[game.active_player_idx].output()

        if args is not None:
            game.turn(args)


def n_games(game_num):
    wist_game = WistGame(False)
    scores = wist_game.PLAYERS_NUMBER*[0]
    for i in range(game_num):
        wist_game = WistGame(False)
        bots = 4 * [None]
        RoundNum = 1
        version = 1
        for idx in range(wist_game.PLAYERS_NUMBER):
            bots[idx] = RandomAI(wist_game, wist_game.players[idx])
        bots[3] = MaxNAI(wist_game, wist_game.players[3], RoundNum, version)

        score = bot_game(bots, wist_game)
        scores = [score[i] + scores[i] for i in range(len(scores))]
    return scores

print(n_games(1000))