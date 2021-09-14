import re

from pytest import mark as m
import pytest
from tbs.board.board import Position, PositionObstructedError
from tbs.entity.entity import (
    Entity,
    DifferentEntityError,
    MissingCreateOrderError,
    OrderOutOfBoundsError,
)
from .entity_fixtures import (
    test_position,
    test_entity,
    test_entity_with_order,
    not_test_entity,
    test_order,
    TestOrder,
)

TestOrder.__test__ = False  # Tell pytest not to attempt collection


@m.describe("Entity")
class TestEntity(object):
    @m.context("When order lists are the same")
    @m.it("Can equate to the same entity")
    def test_equals_identical(self, test_entity):
        assert test_entity == test_entity

    @m.context("When order lists are different lengths")
    @m.it("Can equate to the same entity")
    def test_equals_new_order(self, test_entity, test_entity_with_order):
        assert test_entity == test_entity_with_order

    @m.context("When order lists are different lengths")
    @m.it("Can compare with the same entity to determine which is older")
    def test_comparison(self, test_entity, test_entity_with_order):
        assert test_entity < test_entity_with_order
        assert not test_entity > test_entity_with_order

    @m.it("Cannot equate to a different entity")
    def test_not_equals(self, test_entity, not_test_entity):
        assert test_entity != not_test_entity

    @m.it("Raises an error when comparing different entities")
    def test_compare_different(self, test_entity, not_test_entity):
        with pytest.raises(
            DifferentEntityError,
            match=re.escape(r"{} vs {}".format(test_entity, not_test_entity)),
        ):
            test_entity < not_test_entity
        with pytest.raises(
            DifferentEntityError,
            match=re.escape(r"{} vs {}".format(test_entity, not_test_entity)),
        ):
            test_entity > not_test_entity

    @m.context("When creation position is empty")
    @m.it("Returns creation position")
    def test_create_empty(self, test_entity, test_position):
        assert test_entity.create() == test_position

    @m.context("When creation position is obstructed")
    @m.it(
        "Raises an error"
    )  # TODO: may want to add to this later (create in nearest possible location?
    def test_create_obstructed(self, test_entity):
        _ = test_entity.create()
        create_target = test_entity.order(0).target
        with pytest.raises(
            PositionObstructedError,
            match=r"^Could not create entity at x:{} y:{} turn:{}".format(
                create_target.x, create_target.y, create_target.t
            ),
        ):
            test_entity.create()

    @m.context("If the Create order has been replaced")
    @m.it("Raises an error")
    def test_create_error(self, test_entity, test_order):
        test_entity._orders[0] = test_order
        with pytest.raises(
            MissingCreateOrderError,
            match=r"^The create order for this entity is missing",
        ):
            test_entity.create()

    @m.context("When attempting to change out of bounds order")
    @m.it("Raises an error")
    def test_change_oob(self, test_entity, test_order):
        with pytest.raises(
            OrderOutOfBoundsError, match=r"^Cannot change order prior to turn 0"
        ):
            test_entity.change_order(-2, test_order)

    @m.context("When orders are linear")
    @m.it("Can get order on a given turn")
    def test_order_selection_linear(
        self, test_entity_with_order, test_order, test_position
    ):
        assert test_entity_with_order.order(0) == Entity.Create(test_position)
        assert test_entity_with_order.order(1) == test_order

    @m.context("When orders include reverse time travel")
    @m.it("Can get order on a given turn")
    def test_order_selection_non_linear(
        self, test_entity_with_order, test_position, test_order
    ):
        for i in range(4):
            test_entity_with_order.give_order(test_order)
        time_travel_order = TestOrder(test_position, -3)
        test_entity_with_order.give_order(time_travel_order)
        diff_test_order = TestOrder(Position(test_position.board, 1, 1), 1)
        for i in range(2):
            test_entity_with_order.give_order(diff_test_order)
        assert test_entity_with_order.order(1) == test_order
        assert test_entity_with_order.order(6) == time_travel_order
        assert test_entity_with_order.order(3) == diff_test_order
