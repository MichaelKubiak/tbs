from classes.entity import Entity, Team
from typing import Tuple, List
from classes.board import Board, SpaceFullError


class Unit(Entity):
    """
    Base class for units
    """
    def __init__(self, pos: Tuple, team: Team, board: Board):
        self._dead = False
        super().__init__(pos, team, board)
        self._history = [self._pos]
        self._moved = False

    def get_pos(self, t) -> Tuple:
        return self.get_history()[t].as_tuple()

    def destroy(self):
        self._dead = True
        self._history.append(self._pos)
        self._pos = None

    def is_dead(self) -> bool:
        return self._dead

    def move(self, x: int, y: int):
        if self.moved():
            raise MovedError
        if (x, y) in self._board.full(self._pos.get_t() + 1):
            raise SpaceFullError
        self._history.append(self._pos)
        self._pos.move(x, y, 1)
        self._moved = True

    def moved(self) -> bool:
        return self._moved

    def refresh(self):
        self._moved = False

    def get_history(self) -> List[Entity.Position]:
        return self._history

    def set_board(self, board: Board):
        self._board = board
        self._board.add_entity(self)


class MovedError(Exception):
    """
    Raise this when a unit tries to move a second time without being 
    refreshed
    """
