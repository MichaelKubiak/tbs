from __future__ import annotations
from typing import Tuple
from abc import ABC, abstractmethod
from classes.board import Board
from enum import Enum, auto


class Team (Enum):
    RED = auto()
    BLUE = auto()
    YELLOW = auto()


class Entity(ABC):
    """
    Abstract base class for entities including:
    - Units
    - Structures
    """
    nextID = 0
    maxHealth = 100
    
    def __init__(self, pos: Tuple, team: Team, board: Board):
        self._ID = Entity.nextID
        Entity.nextID += 1
        self._health = Entity.maxHealth
        self._team = team
        self._board = board
        self._board.set_changed(pos[2])
        self._pos = self.Position(pos, board.get_turn())

    def get_ID(self) -> int:
        return self._ID

    def get_pos(self, t) -> Tuple or None:
        if self._pos is not None:
            return self._pos.as_tuple()
        else:
            return None

    def get_health(self) -> int:
        return self._health

    def get_team(self) -> Team:
        return self._team

    def damage(self, damage: int):
        self._health -= damage
        if self._health <= 0:
            self.destroy()

    def repair(self, repair: int):
        self._health = min(Entity.maxHealth, self._health + repair)

    @abstractmethod
    def destroy(self):
        pass
    
    class Position:
        def __init__(self, pos: Tuple, t: int):
            self._x = pos[0]
            self._y = pos[1]
            self._t = t

        def move(self, x: int, y: int, t: int):
            self._x += x
            self._y += y
            self._t += t

        def as_tuple(self) -> Tuple:
            return self._x, self._y, self._t

        def get_x(self) -> int:
            return self._x

        def get_y(self) -> int:
            return self._y

        def get_t(self) -> int:
            return self._t
