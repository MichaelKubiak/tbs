from __future__ import annotations
from typing import List


class Board:
    """
    The board on which the game takes place
    """

    _x: int
    _y: int
    # _tiles
    _states: List[List[List[bool]]]  # TODO: FIND A BETTER WAY TO DO THIS

    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y
        self._states = [[x * [y * True]]]

    @property
    def states(self):
        return self._states

    def state(self, turn: int):
        """
        Returns a 2d state array for the provided turn

        Args:
            turn: the turn for which to provide a state matrix

        Returns: List[List[bool]]
        """
        return self.states[turn]

    def pos_state(self, pos):
        return self.state(pos.t)[pos.x][pos.y]

    def set_state(self, pos: Position, value: bool):
        self.state(pos.t)[pos.x][pos.y] = value

    def empty(self, pos: Position):
        return self.states[pos.t][pos.x][pos.y]

    def occupy(self, pos: Position):
        self.set_state(pos, False)


class Position(object):
    """
    An object denoting a space-time position on a board
    """

    _x: int
    _y: int
    _t: int
    _board: Board

    def __init__(self, board: Board, x: int, y: int, t: int = None):
        self._board = board
        self._x = x
        self._y = y
        self._t = t

    def __eq__(self, other):  # Do I need to test board equality?
        if type(other) is type(self):
            return self.pos == other.pos and self.t == other.t
        return False

    def __str__(self):
        return "x:{} y:{} turn:{}".format(self.x, self.y, self.t)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def t(self):
        return self._t

    @property
    def pos(self):
        return self.x, self.y

    @property
    def board(self):
        return self._board

    @property
    def is_empty(self):
        return self.board.empty(self)

    def occupy_position(self):
        self.board.occupy(self)


class PositionObstructedError(Exception):
    """
    Raise when an order attempts to move or create an entity at an obstructed
    position
    """

    pass
