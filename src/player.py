import config

class Player:
    # Symbol för spelaren (används dock inte direkt här,
    # utan "@"" ritas i Grid.__str__)
    # Marker = "@"

    def __init__(self, x, y,start_score):
        # Startposition och poäng
        self.pos_x = x
        self.pos_y = y
        self.score = start_score
        self.inventory =[]
        self.grace_counter = 0

    # ------------------------
    # SCORE
    # ------------------------

    def adjust_score(self, amount):
        self.score = self.score + amount

    def apply_step_penalty(self, penalty):

        if self.grace_counter > 0:
            self.grace_counter -= 1
        else:
            self.adjust_score(penalty)

    # ------------------------
    # INVENTORY
    # ------------------------

    def add_item(self, item):
        self.inventory.append(item)
        self.adjust_score(item.value)
        self.grace_counter = config.grace_steps

    def show_inventory(self):
        return ", ".join(item.name for item in self.inventory)

    def has_item(self, item_name):
        return any(i.name == item_name for i in self.inventory)

    # ------------------------
    # MOVEMENT
    # ------------------------

    def move(self, dx, dy):
        """Flyttar spelaren.\n
        dx = horisontell förflyttning, från vänster till höger\n
        dy = vertikal förflyttning, uppifrån och ned"""

        self.pos_x += dx
        self.pos_y += dy

    def can_move(self, dx, dy, grid):
        """
        Kontrollerar om spelaren får flytta sig och det inte finns vägg som hinder.
        """
        new_x = self.pos_x + dx
        new_y = self.pos_y + dy

        # Kontrollera att vi inte går utanför spelplanen (både x och y). Returnerar false
        if new_x < 0 or new_x >= grid.width:
            return False

        if new_y < 0 or new_y >= grid.height:
            return False

        cell = grid.get(new_x, new_y)

        # Om det är en yttervägg – alltid stop
        if cell == grid.exterior_wall:
            return False

        # Innervägg
        if cell == grid.internal_wall:

            # Leta efter item med breaks_wall-egenskap
            for item in self.inventory:
                if item.properties.get("breaks_wall"):
                    grid.remove_connected_wall(new_x, new_y)        # Tar bort hela väggen
                    self.inventory.remove(item)
                    return True
            return False

        return True




