# Konfigurationsfil med alla fasta värden

#----------------------------------------------
# Grid konfiguration
#______________________________________________

# Spelplanen
grid_width = 36  # Bredd på spelplanen
grid_height = 12  # Höjd på spelplanen
grid_empty = "."  # Tecken för en tom ruta
grid_exterior_wall = "■"  # Ytterväggar
grid_internal_wall = "▓" # Innerväggar

# Intern vägg i spelplanen
internal_wall_rows = [grid_height // 2]
internal_wall_columns = [grid_width // 3]


#----------------------------------------------
# Player konfiguration
#______________________________________________

player_start_x = grid_width // 2
player_start_y = grid_height // 2
player_start_score = 10
player_mark ="@"
player_step_penalty = -1

# ----------------------------------------------
# Movement configuration
# ----------------------------------------------

movements = {
    "d": (1, 0),
    "a": (-1, 0),
    "w": (0, -1),
    "s": (0, 1)
}

# ----------------------------------------------
# Commands
# ----------------------------------------------

commands = {
    "inventory": "i",
    "bomb": "b",
    "disarm_trap": "t",
    "quit": ["q", "x"]
}

#----------------------------------------------
# Items konfiguration
#______________________________________________

default_item_value = 20
default_item_symbol = "?"
default_trap_value = -10

grace_steps = 5

bomb_timer = 3
bomb_damage = -20

items = {
    "carrot": {
        "value": default_item_value,
        "symbol": default_item_symbol},
    "apple": {
        "value": default_item_value,
        "symbol": default_item_symbol},
    "strawberry": {
        "value": default_item_value,
        "symbol": default_item_symbol},
    "cherry": {
        "value": default_item_value,
        "symbol": default_item_symbol},
    "watermelon": {
        "value": default_item_value,
        "symbol": default_item_symbol},
    "radish": {
        "value": default_item_value,
        "symbol": default_item_symbol},
    "cucumber": {
        "value": default_item_value,
        "symbol": default_item_symbol},
    "meatball": {
        "value": default_item_value,
        "symbol": default_item_symbol},

    # Special-items
    "shovel": {
        "value": 0,
        "breaks_wall": True,
        "symbol": "S"},
    "trap": {
        "value": default_trap_value,
        "is_trap": True,
        "symbol": "X"},
    "bomb": {
        "value": 0,
        "symbol": "B",
        "is_bomb": True}
}

# Hur många av varje item som ska slumpas ut
item_spawn_count = {
    "trap": 3,
    "shovel": 1,
    "bomb": 1
}