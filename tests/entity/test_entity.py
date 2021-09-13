from pytest import mark as m
import pytest
from tbs.board.board import PositionObstructedError
from entity_fixtures import test_position, test_entity


@m.describe("Entity")
class TestEntity(object):
    @m.context("When creation position is empty")
    @m.it("Returns creation position")
    def test_create_empty(self, test_entity, test_position):
        assert test_entity.order(0).execute() == test_position

    @m.context("When creation position is obstructed")
    @m.it("Raises an error")  # may want to add to this later
    def test_create_obstructed(self, test_entity):
        entity = test_entity
        _ = entity.order(0).execute()
        with pytest.raises(
            PositionObstructedError,
            match=r"^Could not create entity at x:{} y:{} turn:{}".format(0, 0, 0),
        ):
            entity.order(0).execute()
