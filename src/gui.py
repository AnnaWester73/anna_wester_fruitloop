
def print_status(game):
    print("--------------------------------------")
    print(f"You have {game.player.score} points.")
    print(game.grid)

def print_controls():
    print("Use WASD to move")
    print("I = Inventory")
    print("B = Place bomb")
    print("T = Disarm trap")
    print("Q/X = Quit")

def print_inventory(player):
    inv = player.show_inventory()
    print("--------------------------------------")
    print("Your inventory:")
    print(inv if inv else "Empty")

def print_item_found(name, value):
    print(f"You found a {name}, +{value} points.")

def print_trap(value):
    print(f"You stepped on a trap! {value} points.")

def print_bomb_placed():
    print("Bomb is placed!")

def print_bomb_exploded():
    print("BOOM! BOOM! BOOM!")

def print_player_hit_by_explosion(damage):
    print(f"You were in the explosion! {damage} points.")

def print_trap_disarmed():
    print("Trap disarmed!")


def print_game_over(score):
    print("--------------------------------------")
    print("GAME OVER")
    print(f"Final score: {score}")

def print_exit_message():
    print("Thank you for playing!")