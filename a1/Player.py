from __future__ import annotations
from Pieces import Pieces
from Style import Style
from typing import Dict, List, Tuple, Union
from Turn import Turn
from random import randint


class Player:
    """
    # TODO: Complete class documentation
    """
    # TODO: Add class attribute type annotations
    player_id: str

    # TODO: Add method type annotations
    def __init__(self, player_id: str) -> None:
        """
        # TODO: Complete method documentation
        """
        self.player_id = player_id

    # TODO: Add method type annotations
    def get_turn(self):
        """
        # TODO: Complete method documentation
        """
        raise NotImplementedError

    # TODO: Add method type annotations
    def get_tokens(self) -> List[Tuple[int, int]]:
        """
        # TODO: Complete method documentation
        """
        board = self.onitama.get_board()
        tokens = []
        for i, row in enumerate(board):
            for j, token in enumerate(row):
                if token.lower() == self.player_id.lower():
                    tokens.append((i, j))
        return tokens

    # TODO: Add method type annotations
    def get_styles(self):
        """
        # TODO: Complete method documentation
        """
        styles = []
        for sty in self.onitama.get_styles():
            if sty.owner == self.player_id:
                styles.append(sty)
        return styles

    # TODO: Add method type annotations
    def get_valid_turns(self):
        """
        # TODO: Complete method documentation
        """
        styles = self.get_styles()
        tokens = self.get_tokens()
        turns = {}
        for sty in styles:
            turns[sty.name] = []
            for row, col in tokens:
                for d_row, d_col in sty.get_moves():
                    # Flip move direction if player is X
                    if self.player_id == Pieces.G1:
                        d_row *= -1
                        d_col *= -1
                    # Check is_legal_move
                    if self.onitama.is_legal_move(row, col, row + d_row, col + d_col):
                        turns[sty.name].append(Turn(row, col, row + d_row,
                                                    col + d_col, sty.name, self.player_id))

        return turns

    # TODO: Add method type annotations
    def set_onitama(self, onitama) -> None:
        """
        # TODO: Complete method documentation
        """
        self.onitama = onitama


class PlayerRandom(Player):
    """
    # TODO: Complete class documentation
    """

    # TODO: Add method type annotations
    def __init__(self, player_id):
        """
        # TODO: Complete method documentation
        """
        super().__init__(player_id)

    # TODO: Add method type annotations
    def get_turn(self):
        turns = []
        valid_turns = self.get_valid_turns()
        for style_name in valid_turns:
            turns.extend(valid_turns[style_name])

        # Return a random valid turn
        if len(turns) == 0:
            return None
        return turns[randint(0, len(turns) - 1)]
