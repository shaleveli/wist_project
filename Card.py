from enum import Enum, IntEnum
from enum import IntEnum


class Card:
    num = None  # type: CardNum
    symbol = None  # type: CardSymbol
    color = None  # type: Color

    def __init__(self, card_num, card_symbol=None):
        if card_num is None:
            raise ValueError("card_num must be an integer")
        if card_num == CardNum.JOKER and card_symbol is not None:
            raise ValueError("Joker Does not have a symbol")
        else:
            self.num = card_num
            self.symbol = card_symbol
            self.color = color_of_symbol(card_symbol)


class CardNum(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    J = 11
    Q = 12
    K = 13
    ACE = 14
    JOKER = 15


def card_num_to_string(cardnum):
    if cardnum == CardNum.TWO:
        return "2"
    if cardnum == CardNum.THREE:
        return "3"
    if cardnum == CardNum.FOUR:
        return "4"
    if cardnum == CardNum.FIVE:
        return "5"
    if cardnum == CardNum.SIX:
        return "6"
    if cardnum == CardNum.SEVEN:
        return "7"
    if cardnum == CardNum.EIGHT:
        return "8"
    if cardnum == CardNum.NINE:
        return "9"
    if cardnum == CardNum.TEN:
        return "10"
    if cardnum == CardNum.J:
        return "J"
    if cardnum == CardNum.Q:
        return "Q"
    if cardnum == CardNum.K:
        return "K"
    if cardnum == CardNum.ACE:
        return "A"
    if cardnum == CardNum.JOKER:
        return "JOKER"


class CardSymbol(Enum):
    HEART = 1
    CLUB = 2
    SPADE = 3
    DIAMOND = 4


def card_symbol_to_string(cardsym):
    if cardsym == CardSymbol.HEART:
        return "H"
    if cardsym == CardSymbol.CLUB:
        return "C"
    if cardsym == CardSymbol.SPADE:
        return "S"
    if cardsym == CardSymbol.DIAMOND:
        return "D"


def card_to_string(card):
    return card_num_to_string(card.num) + card_symbol_to_string(card.symbol)


class Color(Enum):
    RED = 1
    BLACK = 2


def color_of_symbol(symbol):
    if symbol is None:
        return None
    if symbol == CardSymbol.CLUB or symbol == CardSymbol.SPADE:
        return Color.BLACK
    else:
        return Color.RED
