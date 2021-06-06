from __future__ import annotations
from typing import List, Tuple, Union
from Pieces import Pieces


class Style:
    """
    done
    """
    # done
    name: str
    pairs: List[Tuple[int, int]]
    owner: str

    # done
    def __init__(self, pairs, name, owner=Pieces.EMPTY):
        """
        done
        """
        self.name = name
        self._moves = pairs.copy()
        self.owner = owner

    # done
    def get_moves(self) -> List[Tuple[int, int]]:
        """
        done
        """
        return self._moves.copy()

    # done
    def __eq__(self, other: Style) -> True:
        """
        done
        """
        return self.name == other.name and self.owner == other.owner

    # done
    def __copy__(self) -> Style:
        """
        done
        """
        return Style(self._moves.copy(), self.name, self.owner)
