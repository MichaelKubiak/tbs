from __future__ import annotations
from typing import List, Tuple, TYPE_CHECKING
if TYPE_CHECKING:
    from classes.entity import Entity


class Board:

    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height
        self._entities = []
        self._full = []
        self._turn = 0
        self._changed = {0}  # set of turns with a changed board state since the last time unavailable was set
        self.set_full(0)

    def get_width(self) -> int:
        return self._width

    def get_height(self) -> int:
        return self._height

    def get_turn(self) -> int:
        return self._turn

    def add_entity(self, entity: Entity):
        self._entities.append(entity)

    def set_full(self, t: int):
        if len(self._full) < t:
            raise TooManyTurnsError
        full = []
        for entity in self._entities:
            pos = entity.get_pos(t)
            if pos:
                full.append(pos)
        if len(self._full) > t:
            self._full[t] = full
        elif len(self._full) == t:
            self._full.append(full)
        self._changed.remove(t)

    def full(self, t: int) -> List[Tuple]:
        if len(self._full) <= t:
            return []
        if t in self._changed:
            self.set_full(t)
        return self._full[t]

    def set_changed(self, t: int):
        self._changed.add(t)


class SpaceFullError (Exception):
    """
    Raise this when an action that requires an empty space as a
    target, e.g. movement, targets a full space
    """


class TooManyTurnsError(Exception):
    """
    Raise this when something tries to access a turn too far in the
    future
    """
