from . import config

class Player:
    """ Ansvarar för information om spelaren. Klassen används av game.py och grid.py"""

    def __init__(self, x, y,start_score):
        # Initierar spelaren med startposition, startpoäng, Skapar inventory och grace_counter
        self.pos_x = x
        self.pos_y = y
        self.score = start_score
        self.inventory =[]
        self.grace_counter = 0

    # ------------------------
    # SCORE
    # ------------------------

    def adjust_score(self, amount):
        """ Justerar spelarens poäng. Amount kan vara både positivt och negativt.
        Funktion används av add_item(), apply_step_penalty() och logik i game.py
        """
        self.score = self.score + amount

    def apply_step_penalty(self, penalty):
        """ Drar av poäng om inte grace period är aktiv.
        """

        if self.grace_counter > 0:
            self.grace_counter -= 1
        else:
            self.adjust_score(penalty)

    def has_grace(self):
        """Returnerar True om spelaren befinner sig i grace period."""
        return self.grace_counter > 0

    # ------------------------
    # INVENTORY
    # ------------------------

    def add_item(self, item):
        self.inventory.append(item)     # Lägger till item i inventory
        self.adjust_score(item.value)   # Anropar adjust_score() som ökar eller minskar spelarens poäng beroende på items värde

        # Ökar grace med config.grace_steps varje gång.
        # Grace staplas (t.ex. 2 kvar + 5 nya = 7 totalt).
        self.grace_counter = self.grace_counter + config.grace_steps

    def show_inventory(self):
        return ", ".join(item.name for item in self.inventory)      # Returnerar inventory och används vid utskrift

    def has_item(self, item_name):
        return any(i.name == item_name for i in self.inventory)     # Returnerar True om minst ett Item matchar med ett specifikt namn

    # ------------------------
    # MOVEMENT
    # ------------------------

    def move(self, dx, dy):
        """Flyttar spelaren.\n
        dx = horisontell förflyttning, från vänster till höger\n
        dy = vertikal förflyttning, uppifrån och ned.
        Anropas bara om can_move returnerar True"""

        self.pos_x += dx
        self.pos_y += dy

    def can_move(self, dx, dy, grid):
        """
        Kontrollerar om spelaren får flytta sig och det inte finns vägg som hinder.
        Kontrollerar att position är inom griden
        Kontrollerar att det inte är ytterväggar
        Kontrollerar om spelaren har en 'break_wall=True' och få gå igenom innerväggar. Egenskap finns i config.py
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

        # Innervägg kräver spade
        if cell == grid.internal_wall:
            return self.can_break_wall()

        return True

    def can_break_wall(self):
        """ Returnerar True om spelar har ett item med property 'breaks_wall= True'. Egenskap finns i config.py
         """
        for item in self.inventory:
            if item.properties.get("breaks_wall"):
                return True

        return False

    def remove_wall_breaker(self):
        """Tar bort item som kan ta bort interna väggar. Anropas från game.py handle_move()
        """
        for item in self.inventory:
            if item.properties.get("breaks_wall"):
                self.inventory.remove(item)
                return

