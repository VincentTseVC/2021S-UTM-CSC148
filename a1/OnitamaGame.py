from typing import List, Union
from OnitamaBoard import OnitamaBoard
from Player import Player
from Pieces import Pieces
from OnitamaStack import OnitamaStack
from Style import Style


class OnitamaGame:
    """
    An OnitamaGame class consisting of a game board, and keeping track of which player's
    turn it currently is and some statistics about the game (e.g. how many tokens each player
    has). It knows who the winner of the game is, and when the game is over.

    === Attributes === 
    size : the size of this onitama game.
    player1 : Player object representing player 1(Michael).
    player2 : Player object representing player 2(Ilir).
    whose_turn : Player whose turn it is.
    board_stack : A stack of Onitama boards that 

    === Private Attributes ===

    _board: 
        Onitama board object with information on player positions and board layout.

    === Representation Invariants ===
    - Size must be an odd number greater or equal to 5

    """
    size: int
    player1: Player
    player2: Player
    _board: OnitamaBoard
    whose_turn: Player
    onitama_stack: OnitamaStack

    def __init__(self, size: int = 5, player1: Union[Player, None] = None, player2: Union[Player, None] = None) -> None:
        """
        DO NOT MODIFY THIS!!!
        Constructs a game of Onitama with 2 players passed in as parameters
        Sets <whose_turn> to <player1>
        Sets the <self.size> of Onitama to the passed in <size> if valid.

        Precondition: The size must be odd and greater than or equal to 5.
        """
        self.size = size
        self.player1 = player1 if player1 is not None else Player(Pieces.G1)
        self.player2 = player2 if player2 is not None else Player(Pieces.G2)
        self.player1.set_onitama(self)
        self.player2.set_onitama(self)
        self._board = OnitamaBoard(self.size, self.player1, self.player2)
        self.whose_turn = self.player1
        self.onitama_stack = OnitamaStack()

        print(self._board)

    def other_player(self, player: Player) -> Union[Player, None]:
        """
        Given one <player>, returns the other player. If the given <player> is invalid,
        returns null.
        """
        if player.player_id == self.player1.player_id:
            return self.player2
        if player.player_id == self.player2.player_id:
            return self.player1

    def get_token(self, row: int, col: int) -> str:
        """
        Returns the player token that is in the given position, or the empty
        character if no player token is there or if the position provided is invalid.
        """
        return self._board.get_token(row, col)

    def is_legal_move(self, row_o: int, col_o: int, row_d: int, col_d: int) -> bool:
        """
        Checks if a move with the given parameters would be legal based on the
        origin and destination coordinates.
        This method should specifically check for the following 3 conditions:
            1)  The movement is in the bounds of this game's board.
            2)  The correct piece is being moved based on the current player's turn.
            3)  The destination is valid.
                A player CANNOT move on top of their own piece.

        Precondition: <row_o> and <col_o> must be on the board.
        """

        if not (0 <= row_d < self.size and 0 <= col_d < self.size):
            return False
        
        if self.get_token(row_o, col_o).lower() != self.whose_turn.player_id.lower():
            return False
        
        if self.get_token(row_d, col_d).lower() == self.whose_turn.player_id.lower():
            return False
        
        return True


    def move(self, row_o: int, col_o: int, row_d: int, col_d: int, style_name: str) -> bool:
        """
        Attempts to make a move for player1 or player2 (depending on whose turn it is) from
        position <row_o>, <col_o> to position <row_d>, <col_d>. 

        On a successful move, it stores the current (unmodified) state of the board and 
        the list of styles to <self.onitama_stack> by calling the 
        <self.onitama_stack.push(var1, var2)> method.

        After storing the move, it will make the valid move and modify the board and
        actually make the move.

        Returns true if the move was successfully made, false otherwise.

        Preconditon: <row_o> and <col_o> must be on the board.

        Postcondition: A valid move was made on the OnitamaBoard and the correct styles were exchanged.
        """

        # the move is not valid from the conditions in is_legal_move
        if not self.is_legal_move(row_o, col_o, row_d, col_d):
            return False

        # the move does not follow the movement pattern from the given style
        for s in self._board.styles:
            if s.name.lower() == style_name.lower():
                style = s

        f = -1 if self.whose_turn == self.player1 else 1
        reachable = False
        for move in style.get_moves():
            # print(f'({row_o + move[0] * f}, {col_o + move[1] * f}) ({row_d}, {col_d})')
            if row_o + move[0] * f == row_d and col_o + move[1] * f== col_d:
                reachable = True
        
        if not reachable:
            return False
        

        # Store the current state of the board and styles into our OnitamaStack.
        self.onitama_stack.push(self._board.deep_copy(), self._board.get_styles_deep_copy())

        # Exchange the current player's styles.
        self._board.exchange_style(style)

        # Move the token from starting position to the destination position.
        self._board.set_token(row_d, col_d, self._board.get_token(row_o, col_o))
        self._board.set_token(row_o, col_o, Pieces.EMPTY)


        print('Before:', self.whose_turn)
        # Update whose_turn to be the next player's turn.
        self.whose_turn = self.other_player(self.whose_turn)
        print('After:', self.whose_turn)

        print(self._board)


        # return True, since this was a successful operation.
        return True
        



    def get_winner(self) -> Union[Player, None]:
        """
        Returns the winner of the game if the game is over, or the board token for
        EMPTY if the game is not yet finished. As per Onitama's rules, the winner of
        the game is the player whose Grandmaster reaches the middle column on the
        opposite row from the start position, OR the player who captures the other
        player's Grandmaster.
        """

        if self._board.get_token(0, self.size // 2) == self.player2.player_id:
            return self.player2
        
        if self._board.get_token(self.size - 1, self.size // 2) == self.player1.player_id:
            return self.player1

        if self.player2.player_id not in str(self._board):
            return self.player1

        if self.player1.player_id not in str(self._board):
            return self.player2
        
        return Pieces.EMPTY



    def undo(self) -> None:
        """
        DO NOT MODIFY THIS!!!
        Undo's the Onitama game's state to the previous turn's state if possible.
        """
        if not self.onitama_stack.empty():
            # The pop call here returns a board and a list of styles that we use
            # to revert to the previous state of the game
            board, styles = self.onitama_stack.pop()
            self._board.set_board(board)
            self._board.styles = styles
            # Switch to the previous player's turn
            self.whose_turn = self.other_player(self.whose_turn)

    def get_styles(self) -> List[Style]:
        """
        Get the different styles of movement in Onitama, this is the direct reference
        to the styles list.
        """
        return self._board.styles

    def get_styles_deep_copy(self) -> List[Style]:
        """
        DO NOT MODIFY THIS!!!
        Get a DEEP COPY of the different styles of movement in Onitama.
        This makes a new List and has a different memory address than <self._board.styles>
        """
        return self._board.get_styles_deep_copy()

    def get_board(self) -> List[List[str]]:
        """
        DO NOT MODIFY THIS!!!
        Gets a deep copy of this OnitamaBoard.
        """
        return self._board.deep_copy()

    def set_board(self, size: int, board: List[List[str]]) -> None:
        """
        DO NOT MODIFY THIS!!!
        Construct a new OnitamaBoard with the given size and preset board.
        """
        self.size = size
        self._board = OnitamaBoard(
            self.size, self.player1, self.player2, board=board)

    def get_board_string(self) -> str:
        """
        Returns string representation of this board.
        """
        return str(self._board)

    def get_styles_string(self) -> str:
        """
        Returns string representation of all available styles.
        """
        empty_string = 'Fifth style: \n'
        p1_string = f'Player {self.player1.player_id} styles:\n'
        p2_string = f'Player {self.player2.player_id} styles:\n'
        for sty in self.get_styles():
            if sty.owner == self.player1.player_id:
                p1_string += str(sty) + '\n'
            elif sty.owner == self.player2.player_id:
                p2_string += str(sty) + '\n'
            else:
                empty_string += str(sty) + '\n'

        return p1_string + p2_string + empty_string
