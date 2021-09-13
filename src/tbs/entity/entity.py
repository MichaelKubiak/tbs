from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List
from enum import Enum, auto
from tbs.board.board import Position, PositionObstructedError


class Entity(ABC):
    """
    Abstract base class for entity classes including:
    - Units
    - Structures
    """

    _orders: List[Order]
    _team: Team
    _max_health: int

    def __init__(self, team: Team, turn: int, pos: Position):
        self._team = team
        self._health = self._max_health
        self._orders = [Entity.Create(turn, pos)]

    @property
    def team(self):
        """
        The team in the battle to which the entity currently belongs
        """
        return self._team

    @team.setter
    def team(self, new_team: Team):
        self._team = new_team

    @property
    def health(self):
        """
        The current health value of the entity
        """
        return self._health

    @health.setter
    def health(self, value: int):
        self._health = value

    def damage(self, damage: int):
        """
        Cause damage to an entity, if that entity has less than 0 health,
        'destroy' it

        Args:
            damage: the amount of damage done to the entity
        """
        self.health -= damage
        if self.health < 0:
            self.destroy()

    def repair(self, damage: int):
        """
        Increase a unit's current health up to a maximum of its max health

        Args:
            damage: the amount of damage to repair
        """
        self.health = min(self.max_health, self.health + damage)

    @property
    def start_pos(self):
        return self.orders[0].target.pos

    @property
    def created(self):
        return self.orders[0].length

    @property
    def orders(self):
        """
        The list of Orders given to the entity since it was created, beginning
        with a Create Order, which says where and when it was created.
        """
        return self._orders

    def order(self, turn: int):
        """
        TODO: WORK OUT HOW MULTIPLE ORDERS ON A TURN WORK (maybe last time that an order ends on a turn?)
        Gets the order given on turn
        """
        return self._orders[turn + self.created]

    def give_order(self, order: Order):
        self._orders.append(order)

    def change_order(self, turn: int, order: Order):
        self._orders[turn + self.created] = order

    @property
    @abstractmethod
    def max_health(self):
        pass

    @abstractmethod
    def pos(self, turn: int):
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
        _length: int

        def __init__(self, target: Position):
            self._target = target

        @property
        def target(self):
            """
            The target Position for the order, could be:
            - An empty square to move into
            - An enemy unit to fire upon
            - A friendly unit to repair
            - etc.
            """
            return self._target

        @property
        @abstractmethod
        def length(self):
            """
            The number of turns that the order takes to complete
            """
            return self._length

        @abstractmethod
        def execute(self):
            """
            Check that the order is possible (nothing in the way), then perform
            the action
            """
            pass

    class Create(Order):
        """
        Create order, determines where and when the entity is created
        """

        def __init__(self, turn: int, pos: Position):
            self.length = turn
            super().__init__(pos)

        @property
        def length(self):
            return super().length

        @length.setter
        def length(self, turn):
            self._length = turn

        def execute(self):
            """
            Returns the starting position of the entity if that is an allowable
            position

            Returns: Position
            """
            start_pos = Position(
                self.target.board, self.target.x, self.target.y, self.length
            )
            if start_pos.is_empty:
                start_pos.occupy_position()
                return start_pos
            else:
                raise PositionObstructedError(
                    "Could not create entity at {}".format(start_pos)
                )

    class Team(Enum):
        RED = auto()
        BLUE = auto()
        YELLOW = auto()
        NEUTRAL = auto()
