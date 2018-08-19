def approx_rounds_simple(cards, trump_symbol):
    rounds = 0
    for c in cards:
        if c.symbol == trump_symbol:
            TEN_CARD_VALUE = 10
            if c.value >= TEN_CARD_VALUE:  # 10,J,K,Q,A
                rounds = rounds + 1
        else:
            Q_CARD_VALUE = 12
            if c.value >= Q_CARD_VALUE:  # Q,K,A
                rounds = rounds + 1
    return rounds

