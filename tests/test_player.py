from src.player import Player
from src.pickups import Item


def test_adjust_score():
    player = Player(0, 0, 10)
    player.adjust_score(5)
    assert player.score == 15


def test_step_penalty_without_grace():
    player = Player(0, 0, 10)
    player.apply_step_penalty(-1)
    assert player.score == 9


def test_step_penalty_with_grace():
    player = Player(0, 0, 10)
    player.grace_counter = 2
    player.apply_step_penalty(-1)
    assert player.score == 10
    assert player.grace_counter == 1


def test_add_item_increases_score_and_inventory():
    player = Player(0, 0, 10)
    item = Item("carrot", 20, "?")

    player.add_item(item)

    assert player.score == 30
    assert "carrot" in player.show_inventory()


def test_can_break_wall_when_has_shovel():
    player = Player(0, 0, 0)
    shovel = Item("shovel", 0, "S", {"breaks_wall": True})
    player.add_item(shovel)

    assert player.can_break_wall() is True


def test_remove_wall_breaker():
    player = Player(0, 0, 0)
    shovel = Item("shovel", 0, "S", {"breaks_wall": True})
    player.add_item(shovel)

    player.remove_wall_breaker()

    assert player.can_break_wall() is False

def test_has_grace_true():
    player = Player(0, 0, 0)
    player.grace_counter = 3
    assert player.has_grace() is True


def test_has_grace_false():
    player = Player(0, 0, 0)
    assert player.has_grace() is False


def test_show_inventory_empty():
    player = Player(0, 0, 0)
    assert player.show_inventory() == ""


def test_has_item_true():
    player = Player(0, 0, 0)
    item = Item("carrot", 20, "?")
    player.add_item(item)

    assert player.has_item("carrot") is True


def test_has_item_false():
    player = Player(0, 0, 0)
    assert player.has_item("carrot") is False