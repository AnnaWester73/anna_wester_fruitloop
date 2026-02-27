import random               # Används för att slumpa positioner på spelplanen
import config

class Grid:
    """Representerar spelplanen. Du kan ändra standardstorleken och tecknen för olika rutor. """

    def __init__(self):
        """Skapa ett objekt av klassen Grid"""
        # Spelplanen lagras i en lista av listor. Vi använder "list comprehension" för att sätta tecknet för "empty" på varje plats på spelplanen.
        self.width = config.grid_width
        self.height = config.grid_height
        self.empty = config.grid_empty
        self.exterior_wall = config.grid_exterior_wall
        self.internal_wall = config.grid_internal_wall

        self.data = [[self.empty for _ in range(self.width)] for _ in range(
            self.height)]


    def get(self, x, y):
        """Hämta det som finns på en viss position (x, y)"""
        return self.data[y][x]      # Först rad (y), sedan kolumn (x)

    def set(self, x, y, value):
        """Ändra vad som finns på en viss position"""
        self.data[y][x] = value

    def set_player(self, player):
        """Koppla en spelare till spelplanen"""
        self.player = player

    def clear(self, x, y):
        """Ta bort item från position genom att sätta den till tom"""
        self.set(x, y, self.empty)

    def __str__(self):
        """Gör så att vi kan skriva ut spelplanen med print(grid). Bygger upp en sträng rad för rad."""
        xs = ""

        for y in range(len(self.data)):
            row = self.data[y]
            for x in range(len(row)):
                # Om spelaren står på denna position – skriv "@"
                if x == self.player.pos_x and y == self.player.pos_y:
                    xs += config.player_mark
                else:
                    xs += str(row[x])       # Annars skriv det som finns i rutan
            xs += "\n"                      # Ny rad efter varje rad i spelplanen
        return xs

    # =========================
    # EXTERNAL WALLS
    # =========================

    def make_exterior_walls(self):

        for i in range(self.height):
            self.set(0, i, self.exterior_wall)
            self.set(self.width - 1, i, self.exterior_wall)

        for j in range(1, self.width - 1):
            self.set(j, 0, self.exterior_wall)
            self.set(j, self.height - 1, self.exterior_wall)

    # =========================
    # INTERNAL WALLS
    # =========================

    def place_internal_wall(self, x, y):
        """
        Sätter en innervägg om rutan är tillåten.
        """
        # Bygger bara på tom ruta
        if not self.is_empty(x, y):
            return

        # Bygg aldrig innervägg på spelarens startposition
        if x == config.player_start_x and y == config.player_start_y:
            return

        self.set(x, y, self.internal_wall)

    def make_internal_walls(self):
        """ Skapar sammanhängande interna väggar som slumpas ut.
        Blockerar aldrig spelarens startposition.
        """

        mid_x = self.width // 2
        base_y = self.height - 3

        u_height = self.height // 4
        u_width = self.width // 6

        # Vänster sida
        for y in range(base_y - u_height, base_y):
            self.place_internal_wall(mid_x - u_width // 2, y)

        # Höger sida
        for y in range(base_y - u_height, base_y):
            self.place_internal_wall(mid_x + u_width // 2, y)

        # Botten
        for x in range(mid_x - u_width // 2,
                       mid_x + u_width // 2 + 1):
            self.place_internal_wall(x, base_y)

    # =========================
    # WALL REMOVAL
    # =========================

    def remove_connected_wall(self, x, y):

        target = self.internal_wall
        stack = [(x, y)]

        while stack:
            cx, cy = stack.pop()

            if cx < 0 or cx >= self.width:
                continue
            if cy < 0 or cy >= self.height:
                continue
            if self.get(cx, cy) != target:
                continue

            self.clear(cx, cy)

            stack.append((cx + 1, cy))
            stack.append((cx - 1, cy))
            stack.append((cx, cy + 1))
            stack.append((cx, cy - 1))

    def explode_area(self, x, y):
        """
        Förstör allt i ett 3x3 område runt (x, y).
        """

        destroyed_positions = []

        for dx in range(-1, 2):
            for dy in range(-1, 2):

                nx = x + dx
                ny = y + dy

                if 0 <= nx < self.width and 0 <= ny < self.height:

                    # Ta bort allt utom ytterväggar
                    if self.get(nx, ny) != self.exterior_wall:
                        self.clear(nx, ny)
                        destroyed_positions.append((nx, ny))

        return destroyed_positions

    # =========================
    # RANDOM
    # =========================

    # Används i filen pickups.py
    def get_random_x(self):
        """Slumpa en x-position på spelplanen"""
        return random.randint(0, self.width-1)

    def get_random_y(self):
        """Slumpa en y-position på spelplanen"""
        return random.randint(0, self.height-1)


    def is_empty(self, x, y):
        """Returnerar True om det inte finns något på aktuell ruta (inte vägg eller item"""
        return self.get(x, y) == self.empty