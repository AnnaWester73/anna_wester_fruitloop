import config
import random


class Item:
    """Representerar saker man kan plocka upp."""
    def __init__(self, name, value, symbol, properties=None):
        self.name = name
        self.value = value
        self.symbol = symbol
        self.properties = properties or {}

    def __str__(self):
        return self.symbol


def randomize(grid):
    """
    Skapar Item-objekt från config och placerar dem slumpmässigt.
    """

    for name, data in config.items.items():

        # Hur många exemplar av special items som ska slumpas ut på spelplanen
        count = config.item_spawn_count.get(name, 1)

        for _ in range(count):

            item = Item(
                name=name,
                value=data["value"],
                symbol=data["symbol"],
                properties=data
            )

            # Kollar om det finns en tom cell, så länge det finns läggs ett item ut random.
            empty_cells = grid.get_empty_cells()

            if len(empty_cells) == 0:
                return

            (x, y) = random.choice(empty_cells)
            grid.set(x, y, item)