from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Tuple, TYPE_CHECKING


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
    
    def __init__(self, pos: Tuple, team: Team, entity_id: int = None, health: int = None):
        if not entity_id:
            self._ID = Entity.nextID
            Entity.nextID += 1
        if not health:
            self._health = Entity.maxHealth
        self._team = team
        self._pos = self.Position(pos)

    def get_ID(self) -> int:
        return self._ID

    def get_pos(self) -> Tuple:
        return self._pos.as_tuple()

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

    @abstractmethod
    def apply_order(self):
        pass

    class Position:
        def __init__(self, pos: Tuple):
            self._x = pos[0]
            self._y = pos[1]

        def move(self, x: int, y: int):
            self._x += x
            self._y += y

        def as_tuple(self) -> Tuple:
            return self._x, self._y

        def get_x(self) -> int:
            return self._x

        def get_y(self) -> int:
            return self._y
