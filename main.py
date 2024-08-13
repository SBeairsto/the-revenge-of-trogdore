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

import typing
from collections import Counter
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

    moves = ["up", "down", "right", "left"]
    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    # Step 1 - Extract usefull information from the game_state
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_id = game_state["you"]["id"]

    board_width = game_state['board']['width']
    board_height = game_state['board']['height']
    solo = len(game_state['board']['snakes']) == 1

    my_board = snake_classes.board(board_width, board_height)
    walls = my_board.wall
    all_snakes = snake_classes.snakes(game_state=game_state)
    my_potential_movements = snake_classes.potential_movements(head=my_head)

    ### CHECK FOR UNSAFE MOVES
    # Step 2 - Prevent your Battlesnake from moving out of bounds
    is_move_safe = snake_functions.check_move(is_move_safe,
                                              my_potential_movements,
                                              walls)

    # Step 3 - Prevent your Battlesnake from colliding with itself or
    # other Battlesnakes
    is_move_safe = snake_functions.check_move(is_move_safe,
                                              my_potential_movements,
                                              all_snakes.meat)

    # we will adjust move_rating depending on how beneficial each move is
    move_rating = {'up': 1, 'down': 1, 'left': 1, 'right': 1}

    # if a move is not safe (will cause us to immediately lose) we give it
    # a -100 rating.
    for move, isSafe in is_move_safe.items():
        if not isSafe:
            move_rating[move] = -100

    ### CHOSE BEST MOVE FROM SAFE ONES

    # Step 3 - Prevent your Battlesnake from moving to the same square as
    # a larger snake

    move_rating, enemy_length, enemy_head =\
        snake_functions.avoid_bigger_snakes(move_rating,
                                            game_state,
                                            moves,
                                            my_id,
                                            my_potential_movements)

    # Step 4 - Prevent your Battlesnake from turning into dead ends

    snake_density = []
    for collection in [all_snakes.meat, my_board.wall]:
        for element in collection:
            snake_functions.add_adjacent_positions(element, snake_density)

    # Convert each dictionary to a tuple of its items
    dict_tuples = [tuple(d.items()) for d in snake_density]
    # Count occurrences of each dictionary (as tuples)
    counts = Counter(dict_tuples)
    # Filter dictionaries with at least 3 duplicates
    dense_tiles_1 = [dict(tpl) for tpl, count in counts.items() if count >= 3]
    dense_tiles_1 = snake_functions.remove_matching_dicts(dense_tiles_1, all_snakes.meat)

    move_rating, dense = snake_functions.minimize_distance(my_head,
                                    my_potential_movements,
                                    dense_tiles_1,
                                    move_rating,
                                    board_height,
                                    board_width,
                                    max_dist=2,
                                    weight=-0.1)
    
    dict_tuples = [tuple(d.items()) for d in snake_density]
    # Count occurrences of each dictionary (as tuples)
    counts = Counter(dict_tuples)
    # Filter dictionaries with at least 3 duplicates
    dense_tiles_2 = [dict(tpl) for tpl, count in counts.items() if count >= 4]
    dense_tiles_2 = snake_functions.remove_matching_dicts(dense_tiles_2, all_snakes.meat)
    print(f"The densist tiles are: {dense_tiles_2}")


    move_rating, dense = snake_functions.minimize_distance(my_head,
                                    my_potential_movements,
                                    dense_tiles_2,
                                    move_rating,
                                    board_height,
                                    board_width,
                                    max_dist = 1,
                                    weight=-0.4)



    # Step 4 - Move towards food instead of random, to regain health and survive longer
    food = game_state['board']['food']
    am_I_hungry = True
    am_I_hunting = False
    
    if solo:
        length_diff = 0
    else:
        length_diff = game_state['you']['length'] - enemy_length

    # weight how hungry you are based on how much larger of a snake you are.
    # If you are way bigger, press your advantage
    if length_diff >= 2:
        am_I_hunting = True
        am_I_hungry = False
    else:
        am_I_hunting = False
        am_I_hungry = True

    # if you are low health, you NEED to go get food
    if game_state['you']['health'] < 15:
        am_I_hungry = True
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
    print(f"AM I HUNGRY?: {am_I_hungry}")
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
