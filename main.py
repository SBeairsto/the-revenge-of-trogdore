# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from
# moving backwards.For more info see docs.battlesnake.com

import random
import typing
import snake_classes
import snake_functions
from snake_classes import potential_movements


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "",  # TODO: Your Battlesnake Username
        "color": "#222888",  # TODO: Choose color
        "head": "default",  # TODO: Choose head
        "tail": "default",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_id = game_state["you"]["id"]

    my_potential_movements = snake_classes.potential_movements(head=my_head)

    # Step 1 - Prevent your Battlesnake from moving out of bounds
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']
    my_board = snake_classes.board(board_width, board_height)
    walls = my_board.wall

    is_move_safe = snake_functions.check_move(is_move_safe,
                              my_potential_movements,
                              walls)

    # Step 2 - Prevent your Battlesnake from colliding with itself or
    # other Battlesnakes
    all_snakes = snake_classes.snakes(game_state=game_state)
    is_move_safe = snake_functions.check_move(is_move_safe,
                              my_potential_movements,
                              all_snakes.meat)

    move_rating = {'up': 1, 'down': 1, 'left': 1, 'right': 1}
    for move, isSafe in is_move_safe.items():
        if not isSafe:
            move_rating[move] = -100

    # Choose the best move from the safe ones

    # Step 3 - Prevent your Battlesnake from moving to the same square as
    # a larger snake

    for enemy in game_state['board']['snakes']:
        if enemy['id'] != my_id:
            enemy_potential_movements = snake_classes.potential_movements(enemy['head'])
            enemy_length = enemy['length']
            enemy_head = enemy['head']
            if enemy['length'] >= game_state['you']['length']:
                if my_potential_movements.up in enemy_potential_movements.all:
                    move_rating["up"] -= 0.5
                if my_potential_movements.down in enemy_potential_movements.all:
                    move_rating["down"] -= 0.5
                if my_potential_movements.right in enemy_potential_movements.all:
                    move_rating["right"] -= 0.5
                if my_potential_movements.left in enemy_potential_movements.all:
                    move_rating["left"] -= 0.5

    # Step 4 - Prevent your Battlesnake from turning into dead ends
    snake_density = []
    for element in all_snakes.meat:
        snake_density.append({'x':element['x']+1, 'y': element['y']})
        snake_density.append({'x':element['x']-1, 'y': element['y']})
        snake_density.append({'x':element['x'], 'y': element['y']+1})
        snake_density.append({'x':element['x'], 'y': element['y']-1})
    for element in my_board.wall:
        snake_density.append({'x':element['x']+1, 'y': element['y']})
        snake_density.append({'x':element['x']-1, 'y': element['y']})
        snake_density.append({'x':element['x'], 'y': element['y']+1})
        snake_density.append({'x':element['x'], 'y': element['y']-1})
    
    from collections import Counter
    # Convert each dictionary to a tuple of its items
    dict_tuples = [tuple(d.items()) for d in snake_density]
    # Count occurrences of each dictionary (as tuples)
    counts = Counter(dict_tuples)
    # Filter dictionaries with at least 3 duplicates
    dense_tiles_1 = [dict(tpl) for tpl, count in counts.items() if count >= 3]

    move_rating, dense = snake_functions.minimize_distance(my_head,
                                    my_potential_movements,
                                    dense_tiles_1,
                                    move_rating,
                                    board_height,
                                    board_width,
                                    max_dist=2,
                                    weight=-0.05)
    
    dict_tuples = [tuple(d.items()) for d in snake_density]
    # Count occurrences of each dictionary (as tuples)
    counts = Counter(dict_tuples)
    # Filter dictionaries with at least 3 duplicates
    dense_tiles_2 = [dict(tpl) for tpl, count in counts.items() if count >= 4]

    move_rating, dense = snake_functions.minimize_distance(my_head,
                                    my_potential_movements,
                                    dense_tiles_2,
                                    move_rating,
                                    board_height,
                                    board_width,
                                    max_dist = 2,
                                    weight=-0.2)



    # Step 4 - Move towards food instead of random, to regain health and survive longer
    food = game_state['board']['food']
    am_I_hungry = False
    am_I_hunting = False
    if len(game_state['board']['snakes']) == 1:
        length_diff = 0
    else:
        length_diff = game_state['you']['length'] - enemy_length

    # weight how hungry you are based on how much larger of a snake you are.
    # If you are way bigger, press your advantage
    if game_state['you']['health'] < 15:
        am_I_hungry = True
        am_I_hunting = False
    
    if length_diff >= 2:
        am_I_hunting = True
    else:
        am_I_hunting = False

    if am_I_hungry:
        move_rating, close_food = snake_functions.minimize_distance(my_head,
                                        my_potential_movements,
                                        food,
                                        move_rating,
                                        board_height,
                                        board_width,
                                        max_dist=board_height*board_width,
                                        weight=0.1)

    print(f"AM I HUNTING?: {am_I_hunting}")
    if (am_I_hunting) & (am_I_hungry==False):
        
        move_rating, close_head = snake_functions.minimize_distance(my_head,
                                        my_potential_movements,
                                        [enemy_head],
                                        move_rating,
                                        board_height,
                                        board_width,
                                        max_dist=board_height*board_width,
                                        weight=0.1)

    next_move = max(move_rating, key=move_rating.get)

    #print(f"MOVE {game_state['turn']}: {next_move}")
    #print(f"CLOSEST FOOD: {close_food}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
