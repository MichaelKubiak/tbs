from __future__ import annotations

from abc import ABC, abstractmethod, abstractproperty
from typing import List
from enum import Enum, auto
from tbs.board.board import Position


class Entity(ABC):
    """
    Abstract base class for entities including:
    - Units
    - Structures
    """

    _start_pos: Position
    _orders: List[Order]
    _team: Team
    _max_health: abstractproperty

    def __init__(self, pos: Position, team: Team):
        self._start_pos = pos
        self._orders = []
        self._team = team
        self._health = self._max_health

    def created(self):
        return self._start_pos.t()

    def team(self):
        return self._team

    def health(self):
        return self._health

    def damage(self, damage: int):
        self._health -= damage
        if self._health < self._max_health:
            self.destroy()

    def repair(self, damage):
        self._health = min(self._max_health, self._health + damage)

    @abstractmethod
    def pos(self):
        pass

    @abstractmethod
    def destroy(self):
        pass

    class Order(ABC):
        """
        Abstract base class for orders, these include:
        - Move to [pos]
        - Attack [pos]
        - Perform special building action at [pos]
        """

        _target: Position

        def __init__(self, target: Position):
            self._target = target

        def target(self):
            return self._target

        @abstractmethod
        def perform_order(self):
            pass

    class Team(Enum):
        RED = auto()
        BLUE = auto()
        YELLOW = auto()
        NEUTRAL = auto()
