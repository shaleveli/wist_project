from WistAI import WistAI


class HumanAI(WistAI):

    def __init__(self, game, player=None):
        if player is None:
            WistAI.__init__(self, game, game.players[game.active_player_idx])
        else:
            WistAI.__init__(self, game, player)

    #unuaed
    def card_win(self, card, cards_list):
        """gets a card, and other cards, and check if winning"""
        for c in cards_list:
            if c is not None:
                if not self.game.compare_cards(card, c, card):# added card in case that this is the 1st player and we set the lead
                    return False
        return True

    def card_win_prob(self, card):
        """equal disterbution assumption. winning card devided equally between the players.
         and every player chose by random"""
        no_card_players = 0
        for c in self.info.current_round_cards:
            if c is None:
                no_card_players = no_card_players + 1
        no_card_players = no_card_players - 1  # not including the current player
        win_card_num = 0
        for c in self.info.unseen_cards:
            if not self.game.compare_cards(card, c, card):
                win_card_num = win_card_num + 1
        print(str(card) + " win card num: " + str(win_card_num))
        cards_in_hand = self.info.CARDS_IN_HAND - self.info.game_round + 1

        prob = (1 - win_card_num/(no_card_players * cards_in_hand))**no_card_players
        if not self.card_win(card, self.info.current_round_cards):
            prob = 0
        return prob

    def card_prob_list(self):
        ls = []
        for c in self.info.hand_cards:
            ls.append(self.card_win_prob(c))
        print(ls)

    def __trump_bidding_strategy(self):
        pass
