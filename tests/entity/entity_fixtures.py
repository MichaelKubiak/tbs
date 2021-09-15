import pytest

from tbs.entity.entity import Entity
from tbs.board.board import Position, Board


class TestEntity(Entity):
    def __init__(self, team: Entity.Team, pos: Position):
        self._max_health = 100
        super().__init__(team, pos)
        self._destroyed = False

    @property
    def destroyed(self):
        return self._destroyed

    def pos(self, turn: int):
        pass

    def destroy(self):
        self._destroyed = True


class TestOrder(Entity.Order):
    def __init__(self, target, length):
        super().__init__(target, length)

    def execute(self):
        pass


@pytest.fixture(scope="function")
def test_position():
    return Position(Board(1, 1), 0, 0, 1)


@pytest.fixture(scope="function")
def test_entity(test_position):
    return TestEntity(Entity.Team.RED, test_position)


@pytest.fixture(scope="function")
def test_order(test_position):
    return TestOrder(test_position, 1)


@pytest.fixture(scope="function")
def test_entity_with_order(test_position, test_order):
    entity = TestEntity(Entity.Team.RED, test_position)
    entity.give_order(test_order)
    return entity


@pytest.fixture(scope="function")
def not_test_entity():
    return TestEntity(Entity.Team.RED, Position(Board(1, 1), 1, 0, 0))
