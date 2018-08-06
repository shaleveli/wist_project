class Node:
    data = None
    children = None

    def __init__(self, data, children=None):
        self.data = data
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)

    def add_child(self, node):
        assert isinstance(node, Node)
        self.children.append(node)


class TreeData:
    player_idx = None
    H = None

    def __init__(self, game):
        self.player_idx = game.active_player_idx
        H = [None] * game.PLAYERS_NUMBER
    
