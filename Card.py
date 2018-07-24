from enum import Enum


class Card:
    num = None  #  type: CardNum
    symbol = None  #  type: CardSymbol
    color = None  #  type: Color

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
    ACE = 1
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
    JOKER = 14


class CardSymbol(Enum):
    HEART = 1
    CLUB = 2
    SPADE = 3
    DIAMOND = 4


def all_card_symbols():
    return range(1, 5)


def all_card_nums():
    return range(1, 15)


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
