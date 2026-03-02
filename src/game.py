from .grid import Grid
from .player import Player
from . import pickups
import config
from . import gui


class Game:
    """Ansvarar för spelregler och spel loopar.
    Kopplar samman player.py, grid.py, pickups.py coh gui.py
    Hanterar om man får flytta, poäng, fällor, bomber och avslut av spel
    """
    def __init__(self):
        # Initierar spelet
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

            self.player.move(dx, dy)                                     # Flyttar spelaren
            self.player.apply_step_penalty(config.player_step_penalty)  # Applicera steg straff

            # Väggbrytning
            if self.grid.get(self.player.pos_x, self.player.pos_y) == self.grid.internal_wall:
                self.player.remove_wall_breaker()
                self.grid.remove_connected_line(self.player.pos_x, self.player.pos_y)

            # Kontrollerar om det finns något i rutan
            maybe_item = self.grid.get(self.player.pos_x, self.player.pos_y)

            if isinstance(maybe_item, pickups.Item):

                # Om det finns en fälla
                if maybe_item.properties.get("is_trap"):
                    self.player.adjust_score(maybe_item.value)
                    gui.print_trap(maybe_item.value)

                # Normal item
                else:
                    self.player.add_item(maybe_item)
                    gui.print_item_found(maybe_item.name, maybe_item.value)
                    self.grid.clear(self.player.pos_x, self.player.pos_y)

    # ----------------------------------
    # BOMB LOGIC
    # ----------------------------------

    def place_bomb(self):

        # Kontrollerar om spelaren har en bomb i inventory
        for item in self.player.inventory:
            if item.properties.get("is_bomb"):
                # Lägger till bomb i listan
                self.active_bombs.append({
                    "x": self.player.pos_x,
                    "y": self.player.pos_y,
                    "timer": config.bomb_timer
                })

                # Visar symbol för bomb i spelplanen
                self.grid.set(
                    self.player.pos_x,
                    self.player.pos_y,
                    config.placed_bomb_symbol
                )

                self.player.inventory.remove(item)      # Tar bort bomb från inventory
                gui.print_bomb_placed()                 # Placerar bombens symbol på spelplanen
                return

        # Om ingen bomb hittades
        gui.print_no_bomb()

    def update_bombs(self):

        for bomb in self.active_bombs[:]:

            bomb["timer"] -= 1                          # Minska bombens timer (startvärde från config.bomb_timer)

            if bomb["timer"] <= 0:                      # Explosion av bomb

                gui.print_bomb_exploded()

                destroyed = self.grid.explode_area(bomb["x"], bomb["y"])     # Utlöser explosion i ett 3x3 område

                # Kontrollerar om spelaren står i explosionsområdet när bomben utlöses
                if (self.player.pos_x, self.player.pos_y) in destroyed:
                    self.player.adjust_score(config.bomb_damage)            # Minska spelarens poäng enligt config.bomb_damage
                    gui.print_player_hit_by_explosion(config.bomb_damage)   # Skriver ut att spelaren träffades av explosionen

                self.grid.clear(bomb["x"], bomb["y"])                        # Rensar bombens position på spelplanen

                self.active_bombs.remove(bomb)                               # Tar bort bomben från listan över aktiva bomber

    # ----------------------------------
    # TRAP DISARM
    # ----------------------------------

    def disarm_trap(self):
        """Hanterar fällor.
        """
        # Hämtar spelarens position
        x = self.player.pos_x
        y = self.player.pos_y

        # Hämtar vad som finns på aktuell ruta
        cell = self.grid.get(x, y)

        # Kontrollerar om det är en fälla enligt config.py
        if isinstance(cell, pickups.Item) and cell.properties.get("is_trap"):
            self.grid.clear(x, y)               # Tar bort fällan från spelplanen
            gui.print_trap_disarmed()           # Skriver ut att fällan är borttagen.

    # ----------------------------------
    # COMMAND HANDLER
    # ----------------------------------
    def handle_command(self, command):

        # Rörelsekommando
        if command in config.movements:
            dx, dy = config.movements[command]
            self.handle_move(dx, dy)            # Utför rörelse
            self.update_bombs()                 # Uppdaterar alla aktiva bomber
            return

        # Visar inventory
        if command == config.commands["inventory"]:
            gui.print_inventory(self.player)
            return

        # Placerar bomber
        if command == config.commands["bomb"]:
            self.place_bomb()
            return

        # Desarmerar fällor
        if command == config.commands["disarm_trap"]:
            self.disarm_trap()
            return

    # ----------------------------------
    # GAME LOOP "New function from original"
    # ----------------------------------

    def game_over(self):
        """Ny funktion som inte finns i uppgift. Avslutar spelet när spelare inte har några poäng kvar"""
        return self.player.score < 0

    def run_game(self):

        command = ""

        # Loopa tills användaren trycker Q eller X.
        while command not in config.commands["quit"]:
            gui.print_status(self)      # Skriver ut spelplan och poäng

            command = gui.print_command_prompt()

            self.handle_command(command)

            # ny spelregel som avslutar spelet enligt game_over
            if self.game_over():
                gui.print_game_over(self.player.score)
                break

        gui.print_exit_message()

if __name__ == "__main__":
    game = Game()
    game.run_game()


