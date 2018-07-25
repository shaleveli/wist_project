class Player:
    cards = None  # type: set[Card]
    turn = None  # type: bool
    name = None  # type: string

    def __init__(self, name=None, turn=False):
        self.cards = set()
        self.name = name
        self.turn = turn

    def set_cards(self, card_set=set()):
        self.cards = card_set

    def discard_card(self, card):
        self.cards.remove(card)

    def add_card(self, card):
        self.cards.add(card)
