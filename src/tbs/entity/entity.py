from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import List

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

    def __init__(self, team: Team, pos: Position):
        self._team = team
        self._health = self._max_health
        self._orders = [Entity.Create(pos)]

    def __eq__(self, other):
        if type(other) is type(self):
            return self.created == other.created and self.start_pos == other.start_pos
        return False

    def __lt__(self, other):
        if self == other:
            return len(self.orders) < len(other.orders)
        raise DifferentEntityError("{} vs {}".format(self, other))

    def __gt__(self, other):
        if self == other:
            return len(self.orders) > len(other.orders)
        raise DifferentEntityError("{} vs {}".format(self, other))

    def __str__(self):
        return f"""
            class: {self.__class__.__name__}
            team: {self.team}
            health: {self.health}/{self.health}
            start position: {self.start_pos}
            created: {self.created}
            """

    @property
    def team(self):
        """
        The team to which the entity currently belongs
        """
        return self._team

    @team.setter
    def team(self, new_team: Team):
        self._team = new_team

    @property
    def max_health(self):
        return self.max_health

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

    def create(self):
        create = self.orders[0]
        if create.__class__ == Entity.Create:
            return create.execute()
        else:
            raise MissingCreateOrderError("The create order for this entity is missing")

    @property
    def orders(self):
        """
        The list of Orders given to the entity since it was created, beginning
        with a Create Order, which says where and when it was created.
        """
        return self._orders

    def order(self, turn: int):
        """
        Gets the order given on turn
        """
        order = None
        t = 0
        for o in self.orders:
            if t == turn:
                order = o
            t += o.length
        return order

    def give_order(self, order: Order):
        self.orders.append(order)

    def change_order(self, turn: int, order: Order):
        if turn >= 0 and self.order(0):
            self.orders[turn - self.created] = order
        else:
            raise OrderOutOfBoundsError("Cannot change order prior to turn 0")

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

        def __init__(self, target: Position, length: int):
            self._target = target
            self._length = length

        def __eq__(self, other):
            if type(self) is type(other):
                return self.target == other.target and self.length == other.length

        def __str__(self):
            return f"{self.__class__.__name__} towards {self.target} taking {self.length} turns"

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

        def __init__(self, pos: Position):
            super().__init__(pos, 1)

        def __str__(self):
            return f"Create entity at {self.target} on turn {self.length}"

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
            start_pos = self.target
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


class DifferentEntityError(Exception):
    """
    Raise this when different entities are compared in a way that does not make
    sense
    """


class MissingCreateOrderError(Exception):
    """
    Raise this when the first order of an entity is not a Create order
    """


class OrderOutOfBoundsError(Exception):
    """
    Raise this when an order with negative index would be accessed or changed
    """
