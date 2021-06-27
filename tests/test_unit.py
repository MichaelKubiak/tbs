import pytest
from classes.unit import Unit, MovedError
from classes.board import Board, TooManyTurnsError, SpaceFullError


def test_ID():
    b = Board(8, 8)
    u = Unit((0, 0, 0), "red", b)
    u2 = Unit((0, 1, 0), "blue", b)

    assert u.get_ID() == 0
    assert u2.get_ID() == 1


def test_move():
    b = Board(8, 8)
    u = Unit((0, 0, 0), "red", b)

    assert u.get_pos(-1) == (0, 0, 0)
    u.move(4, 3)
    assert u.get_pos(1) == (4, 3, 1)
    assert u.moved() is True
    try:
        u.move(-2, 1)
        pytest.fail("Should have been unable to move a second time without "
                    "being refreshed")
    except MovedError:
        pass
    u.refresh()
    u.move(-4, -3)
    assert u.get_history() == [(0, 0, 0), (4, 3, 1)]
    assert u.get_pos(-1) == (0, 0, 2)


def test_health():
    b=Board(8,8)
    u = Unit((0, 0, 0), "red")

    # has starting health and position
    assert u.get_health() == 100
    # takes damage
    u.damage(80)
    assert u.get_health() == 20
    # repairs only to max health
    u.repair(100)
    assert u.get_health() == u.maxHealth
    # destroyed and removed from board by losing all health
    u.damage(100)
    assert u.is_dead()
    assert u.get_pos(-1) is None
