from src.pickups import Item


def test_item_init():
    # Testar konstruktor och sätter rätt object
    item = Item("carrot", 20, "?")

    assert item.name == "carrot"
    assert item.value == 20
    assert item.symbol == "?"


def test_item_str_returns_symbol():
    # Testar att rätt symbol returneras
    item = Item("carrot", 20, "?")
    assert str(item) == "?"


def test_item_with_properties():
    # Testar av properties
    item = Item("trap", -10, "X", {"is_trap": True})

    assert item.properties["is_trap"] is True
