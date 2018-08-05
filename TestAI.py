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

    def legal_winner_cards(self, card, lead=None):
        """return ([legal cards],[win cards]) every cell represents a player"""
        # cards in each hand
        cards_in_hand = self.info.CARDS_IN_HAND - self.info.game_round + 1

        # set lead card symbol if its the 1st card
        if self.info.lead_card is not None:
            lead = self.info.lead_card
        lead_sym = lead.symbol

        # Players who need to put cards and players who have
        no_card_players = 0
        lead_card_players = 0
        trump_card_players = 0
        for idx in range(self.info.PLAYERS_NUMBER):
            # Loop over the player who need to put a card
            if idx != self.info.idx:
                if self.info.current_round_cards[idx] is None:
                    no_card_players = no_card_players + 1
                if self.info.player_symbol_list[idx][lead_sym]:
                    lead_card_players = lead_card_players + 1
                if self.info.player_symbol_list[idx][self.info.trump_symbol]:
                    trump_card_players = trump_card_players + 1
        # cards that win Card. Some of them may not be legal
        win_cards_list = []
        for c in self.info.unseen_cards:
            if not self.game.compare_cards(card, c, card):
                win_cards_list.append(c)

        # winners card in lead symbol and every card in lead_sym
        lead_sym_winners = sorted(list(self.player.cards_in_symbol(lead_sym, win_cards_list)))
        trump_sym_winners = sorted(list(self.player.cards_in_symbol(self.info.trump_symbol, win_cards_list)))
        lead_sym_cards = sorted(list(self.player.cards_in_symbol(lead_sym, self.info.unseen_cards)))  # cards in lead symbol
        win_card_num = len(win_cards_list)

        # estimation of each player legal card sum and winning cards in the hand
        legal_players_cards = self.info.PLAYERS_NUMBER * [None]
        win_players_cards = self.info.PLAYERS_NUMBER * [None]

        mod_lead = len(lead_sym_cards) % lead_card_players  # extra card to devide between players
        mod_trump_winner = len(trump_sym_winners) % trump_card_players
        mod_lead_winner = len(lead_sym_winners) % lead_card_players
        for idx in range(self.info.PLAYERS_NUMBER):
            # if player is us or player that already placed a card: pass
            if idx == self.info.idx or self.info.current_round_cards[idx] is not None:
                continue
            # if player doesnt have symbol everything is legal and if he have trump cards...
            if not self.info.player_symbol_list[idx][lead_sym] and self.info.player_symbol_list[idx][self.info.trump_symbol]:
                legal_players_cards[idx] = cards_in_hand
                win_players_cards[idx] = len(trump_sym_winners) // trump_card_players
                if mod_trump_winner > 0:
                    win_players_cards[idx] = win_players_cards[idx] + 1
                    mod_trump_winner = mod_trump_winner - 1
            elif self.info.player_symbol_list[idx][lead_sym]:  # if player has lead card symbol
                legal_players_cards[idx] = len(lead_sym_cards) // lead_card_players
                win_players_cards[idx] = len(lead_sym_winners) // lead_card_players
                if mod_lead > 0:
                    legal_players_cards[idx] = legal_players_cards[idx] + 1
                    mod_lead = mod_lead - 1
                if mod_lead_winner > 0:
                    win_players_cards[idx] = win_players_cards[idx] + 1
                    mod_lead_winner = mod_lead_winner - 1
            else: # if player doesnt have lead or trump
                legal_players_cards[idx] = cards_in_hand
                win_players_cards[idx] = 0
        return legal_players_cards, win_players_cards

    def card_win_prob(self, card):
        """equal disterbution assumption. winning card devided equally between the players.
         and every player choose by random"""
        no_card_players = 0
        for c in self.info.current_round_cards:
            if c is None:
                no_card_players = no_card_players + 1
        no_card_players = no_card_players - 1  # not including the current player
        if no_card_players == 0:  # if the player is the last one in the round
            if self.card_win(card, self.info.current_round_cards):
                prob = 1
            else:
                prob = 0
            return prob
        print(str(card) + ' ' + str(self.legal_winner_cards(card, card)))
        if not self.card_win(card, self.info.current_round_cards):
            prob = 0
        #return prob

    def card_prob_list(self):
        ls = []
        for c in sorted(list(self.player.legal_play(self.info.lead_card))):
            ls.append(self.card_win_prob(c))
        #print(ls)

    def __trump_bidding_strategy(self):
        pass
