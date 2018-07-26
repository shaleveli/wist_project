from WistGame import *


def print_bidding_table(g):
    for row in g.trump_bidding_table:
        s = ""
        for contract in row:
            s += str(contract) + " "
        print(s)


print("TEST WISTGAME:\n")
game = WistGame()
print("created a WistGame\n")

for i in range(game.PLAYERS_NUMBER):
    print("player " + str(i) + " hand:")
    hand_str = ""
    for card in game.players[i].cards:
        hand_str = hand_str + card_to_string(card) + " "
    print(hand_str)

print("\ntesting trump bidding...")
game.turn(WistContract(CardSymbol.HEART, 5))
print(str(game.highest_bidding_contract))

# the following actions should return an error:
# game.turn(WistContract(CardSymbol.SPADE, 4))
# game.turn(WistContract(CardSymbol.CLUB, 5))
# game.turn(WistContract(CardSymbol.HEART, 5))

game.turn(WistContract(CardSymbol.SPADE, 5))
print(str(game.highest_bidding_contract))
game.turn(WistContract())
print(str(game.highest_bidding_contract))
game.turn(WistContract())
print(str(game.highest_bidding_contract))
game.turn(WistContract(CardSymbol.SPADE, 6))
print(str(game.highest_bidding_contract))

# game.turn(WistContract(CardSymbol.HEART, 6))  # error

game.turn(WistContract(CardSymbol.SPADE, 7))
print(str(game.highest_bidding_contract))
game.turn(WistContract(CardSymbol.CLUB, 8))
print(str(game.highest_bidding_contract))
game.turn(WistContract(CardSymbol.SPADE, 8))
print(str(game.highest_bidding_contract))
game.turn(WistContract())
print(str(game.highest_bidding_contract))

# game.turn(WistContract())  #error

print("bidding table:")
print_bidding_table(game)

print("\ntrump symbol is: " + card_symbol_to_string(game.trump_symbol))

print("\ntesting contract bidding...")
# game.turn(7) # error
game.turn(9)  # game.turn(8)  # should also work
game.turn(0)
game.turn(1)
# game.turn(3)  # error
game.turn(4)  # replace with game.turn(2) to get is_under_game == True
# game.turn(2)  # error
for i in range(game.PLAYERS_NUMBER):
    print("player " + str(i) + " final contract: " + str(game.players[i].contract))
print("is_under_game: " + str(game.is_under_game))

print("\ntesting game mode...")
hands = game.PLAYERS_NUMBER*[None]
for i in range(game.PLAYERS_NUMBER):
    hands[i] = list(game.players[i].cards)

for j in range(game.CARDS_IN_HAND):
    print("round num: " + str(j+1))
    for i in range(game.PLAYERS_NUMBER):
        player = game.active_player_idx
        card = list(game.players[player].legal_play(game.lead_card))[0]
        print("player " + str(player) + " draws: " + card_to_string(card))
        game.turn(card)
    print("taker of round " + str(j+1) + ": player " + str(game.takers_history[j]))

print("winners: " + str(game.winners))
print("scores: " + str(game.scores))
print("ended game:" + str(game.ended_game))
print("DONE!")
