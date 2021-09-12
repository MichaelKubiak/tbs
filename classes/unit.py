from classes.entity import Entity, Team
from typing import Tuple, List
from classes.board import Board, SpaceFullError
from copy import deepcopy


class Unit(Entity):
    """
    Base class for units
    """

    def __init__(self, pos: Tuple, team: Team, board: Board):
        self._dead = False
        super().__init__(pos, team, board)
        self._orders = []
        self._moved = False

    def get_pos(self, t: int = -1) -> Entity.Position:
        if t == -1:
            return self._pos()
        turn = self._pos.get_t()
        if t - len(self._orders) < 0:
            raise BeforeCreationError
        else:
            prev_pos = deepcopy(self._pos)
            while turn > t:
                prev_pos.move(self._orders[turn - len(self._orders)].get_move())
                turn -= 1
            return

    def destroy(self):
        self._dead = True

    def is_dead(self) -> bool:
        return self._dead

    def move(self, x: int, y: int):
        if self.moved():
            raise MovedError
        if (x, y) in self._board.full(self._pos.get_t() + 1):
            raise SpaceFullError
        self._pos.move(x, y, 1)
        self._moved = True

    def moved(self) -> bool:
        return self._moved

    def refresh(self):
        self._moved = False

    def apply_order(self):


class MovedError(Exception):
    """
    Raise this when a unit tries to move a second time without being 
    refreshed
    """


class BeforeCreationError(Exception):
    """
    Raise this when a unit's position is requested before it was created
    """
