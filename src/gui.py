
# Skriver ut spelstatus. Hämtar spelarens poäng, skriver ut spelplanen och grace period.
def print_status(game):
    print("--------------------------------------")
    print(f"You have {game.player.score} points.")
    print_controls()
    if game.player.has_grace():
        print(f" Grace {game.player.grace_counter} steg kvar!")
    print(game.grid)
    print("")


def print_controls():
    print("Use WASD to move")
    print("I = Inventory")
    print("B = Place bomb")
    print("T = Disarm trap")
    print("Q/X = Quit")

# Skriver ut spelarens inventory. Hämtar från spelarens. Visar om inventory är tom.
def print_inventory(player):
    inv = player.show_inventory()
    print("--------------------------------------")
    print("Your inventory:")
    print(inv if inv else "Inventory is empty!")

def print_item_found(name, value):
    print(f"You found a {name}, +{value} points.")

def print_trap(value):
    print(f"You stepped on a trap! {value} points.")

def print_bomb_placed():
    print("Bomb is placed!")

def print_bomb_exploded():
    print("BOOM! BOOM! BOOM!")

def print_no_bomb():
    print("You don't have a bomb in your inventory.")

def print_player_hit_by_explosion(damage):
    print(f"You were in the explosion! {damage} points.")

def print_trap_disarmed():
    print("Trap disarmed!")

def print_command_prompt():
    return input("Enter a command: ").casefold()[:1]


def print_game_over(score):
    print("--------------------------------------")
    print("GAME OVER")
    print(f"Final score: {score}")

def print_exit_message():
    print("Thank you for playing!")