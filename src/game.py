from .grid import Grid
from .player import Player
from . import pickups
import config
from . import gui


class Game:
    def __init__(self):
        # Skapar spelaren
        self.player = Player(
            config.player_start_x,
            config.player_start_y,
            config.player_start_score)

        # Skapar spelplanen
        self.grid = Grid()
        self.grid.set_player(self.player)
        self.grid.make_exterior_walls()                 # Skapar ytterväggar
        self.grid.make_internal_walls()                  # Skapar innerväggar

        # Slumpar items at plocka upp.
        pickups.randomize(self.grid)

        self.active_bombs = []

    # ----------------------------------
    # MOVE LOGIC
    # ----------------------------------

    def handle_move(self, dx, dy):
        """Flytta spelaren och plocka upp item om det finns."""
        if self.player.can_move(dx, dy, self.grid):

            new_x = self.player.pos_x + dx
            new_y = self.player.pos_y + dy

            maybe_item = self.grid.get(new_x, new_y)

            self.player.move(dx, dy)
            self.player.apply_step_penalty(config.player_step_penalty)

            if isinstance(maybe_item, pickups.Item):

                #Trap
                if maybe_item.properties.get("is_trap"):
                    self.player.adjust_score(maybe_item.value)
                    gui.print_trap(maybe_item.value)

                # Normal item
                else:
                    self.player.add_item(maybe_item)
                    gui.print_item_found(maybe_item.name, maybe_item.value)
                    self.grid.clear(new_x, new_y)

    # ----------------------------------
    # BOMB LOGIC
    # ----------------------------------

    def place_bomb(self):

        for item in self.player.inventory:
            if item.properties.get("is_bomb"):
                self.active_bombs.append({
                    "x": self.player.pos_x,
                    "y": self.player.pos_y,
                    "timer": config.bomb_timer
                })

                self.player.inventory.remove(item)
                gui.print_bomb_placed()
                return

    def update_bombs(self):

        for bomb in self.active_bombs[:]:

            bomb["timer"] -= 1

            if bomb["timer"] <= 0:

                gui.print_bomb_exploded()

                destroyed = self.grid.explode_area(bomb["x"], bomb["y"])

                # Om spelaren står i explosionen
                if (self.player.pos_x, self.player.pos_y) in destroyed:
                    self.player.adjust_score(config.bomb_damage)
                    gui.print_player_hit_by_explosion(config.bomb_damage)

                self.active_bombs.remove(bomb)

    # ----------------------------------
    # TRAP DISARM
    # ----------------------------------

    def disarm_trap(self):
        x = self.player.pos_x
        y = self.player.pos_y

        cell = self.grid.get(x, y)

        if isinstance(cell, pickups.Item) and cell.properties.get("is_trap"):
            self.grid.clear(x, y)
            gui.print_trap_disarmed()

    # ----------------------------------
    # COMMAND HANDLER
    # ----------------------------------
    def handle_command(self, command):

        # Movement
        if command in config.movements:
            dx, dy = config.movements[command]
            self.handle_move(dx, dy)
            self.update_bombs()
            return

        # Inventory
        if command == config.commands["inventory"]:
            gui.print_inventory(self.player)
            return

        # Bomb
        if command == config.commands["bomb"]:
            self.place_bomb()
            return

        # Disarm trap
        if command == config.commands["disarm_trap"]:
            self.disarm_trap()
            return

    # ----------------------------------
    # GAME LOOP
    # ----------------------------------

    def game_over(self):
        """Returnerar True om spelaren har mindre poäng än 0"""
        return self.player.score < 0

    def run_game(self):

        command = ""

        gui.print_controls()

        # Loopa tills användaren trycker Q eller X.
        while command not in config.commands["quit"]:
            gui.print_status(self)

            # Läs in användarens kommando
            command = input("Command: ").casefold()[:1]

            self.handle_command(command)

            # ny spelregel som avslutar spelet om score < 0
            if self.game_over():
                gui.print_game_over(self.player.score)
                break

        gui.print_exit_message()

if __name__ == "__main__":
    game = Game()
    game.run_game()


