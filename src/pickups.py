import config

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

            while True:
                x = grid.get_random_x()
                y = grid.get_random_y()

                if grid.is_empty(x, y):
                    grid.set(x, y, item)
                    break