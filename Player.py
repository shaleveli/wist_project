class Player:
    cards = None  # type: [Card]
    turn = None  # type: bool
    name = None  # type: string

    def __init__(self, name=None, turn=False):
        self.cards = []
        self.name = name
        self.turn = turn

    def set_cards(self, card_list=[]):
        self.cards = card_list

    def discard_card(self, card):
        self.cards.remove(card)

    def add_card(self, card):
        self.cards.append(card)
