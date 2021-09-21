from __future__ import annotations

from tbs.board.board import Position
from tbs.entity.entity import Entity, Team


class Unit(Entity):
    """
    Abstract base class for unit classes
    """

    _alive: bool
    _speed: int
    _min_range: int
    _max_range: int

    def __init__(self, team: Team, pos: Position):
        self._alive = True
        super().__init__(team, pos)

    def pos(self, turn):
        """
        Apply orders under the current board state to obtain position on a
        specific turn

        Args:
            turn: The turn on which to determine position

        Returns: Position
        """
        t = self.created
        positions = []
        if self.alive:
            pos = self.start_pos
            for order in self.orders:
                if t == turn:
                    positions.append(pos)
                pos = order.execute()
                turn += order.length
            return positions
        return None

    def destroy(self):
        self._alive = False

    def alive(self):
        return self._alive

    def move(self, target: Position):
        """
        Gives this unit a Move order

        Args:
            target: the position to which the unit will move
        """
        self.give_order(Unit.Move(self, target, 1))

    def attack(self, target: Position):
        self.give_order(Unit.Attack(self, target))

    class Move(Entity.Order):
        """
        An order which moves a unit to a specified position can be given by the
        owner, or caused by another unit's attack
        """

        def __init__(self, entity: Unit, target: Position, length: int):
            super().__init__(entity, target, length)

        def execute(self):
            return (
                self._target
            )  # TODO: Check that nothing is in the way, it is within bounds,
            #          and that the path is within movement range (speed)

    class Attack(Entity.Order):
        """
        An order which performs a unit's attack on a specified position
        """

        def __init__(self, entity: Entity, target: Position):
            super().__init__(entity, target, 1)

        def execute(self):
            return self.entity  # TODO: Check that the target is in range, deal damage
