import pytest

from tbs.entity.entity import Entity
from tbs.board.board import Position, Board


class TestEntity(Entity):
    def __init__(self, team: Entity.Team, pos: Position):
        self._max_health = 100
        super().__init__(team, 0, pos)

    @property
    def max_health(self):
        return self

    def pos(self, turn: int):
        pass

    def destroy(self):
        pass


@pytest.fixture(scope="function")
def test_position():
    return Position(Board(1, 1), 0, 0, 0)


@pytest.fixture(scope="function")
def test_entity(test_position):
    return TestEntity(Entity.Team.RED, test_position)
