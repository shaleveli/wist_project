from WistGame import *
from WistBots import *
import cProfile
import numpy
import matplotlib


def bot_game(bots, game, debug=False):
    while 1:
        if game.game_mode == WistGameMode.END:
            return game.scores
        #print(game.active_player_idx)
        args = bots[game.active_player_idx].output()
        if args is not None:
            game.turn(args)


def n_games(game_num):
    wist_game = WistGame(False)
    scores = wist_game.PLAYERS_NUMBER*[0]
    hists = wist_game.PLAYERS_NUMBER * [None]
    for i in range(wist_game.PLAYERS_NUMBER):
        hists[i] = (wist_game.CARDS_IN_HAND + 1) * [0]
    for i in range(game_num):
        wist_game = WistGame(False)
        bots = 4 * [None]
        RoundNum = 2
        version = 1
        for idx in range(wist_game.PLAYERS_NUMBER):
            bots[idx] = RandomAI(wist_game, wist_game.players[idx])
            #bots[idx] = MaxNAI(wist_game, wist_game.players[idx], RoundNum, version)

        score = bot_game(bots, wist_game)
        scores = [score[i] + scores[i] for i in range(len(scores))]

        for idx in range(wist_game.PLAYERS_NUMBER):
            print(wist_game.players[idx].taken_rounds)
            hists[idx][wist_game.players[idx].taken_rounds] = hists[idx][wist_game.players[idx].taken_rounds] + 1

    return scores, hists



print(n_games(1000))
#cProfile.run('n_games(1)')