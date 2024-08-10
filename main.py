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

    class potential_movements:

        def __init__(self, head: typing.Dict) -> typing.Dict:
            self.up = {'x': head['x'], 'y': head['y'] + 1}
            self.down = {'x': head['x'], 'y': head['y'] - 1}
            self.right = {'x': head['x'] + 1, 'y': head['y']}
            self.left = {'x': head['x'] - 1, 'y': head['y']}
            self.all = [self.up, self.down, self.right, self.left]

    class snakes:

        def __init__(self, game_state: typing.Dict) -> typing.Dict:
            self.meat = []
            for snake in game_state["board"]["snakes"]:
                self.meat.extend(snake["body"])

    class board:

        def __init__(self, board_width: int, board_height: int):
            self.wall = []
            for i in range(board_width):
                self.wall.extend([{'x': i, 'y': board_height},
                                  {'x': i, 'y': -1}])
            for i in range(board_height):
                self.wall.extend([{'x': -1, 'y': i},
                                  {'x': board_width, 'y': i}])

            self.density = []
            for i in range(board_width):
                for j in range(board_height):
                    self.density.append({'x': i, 'y': j, 'd': 0}),


    def check_move(is_move_safe: typing.Dict,
                   my_potential_movements: potential_movements,
                   obstacles: typing.Dict) -> typing.Dict:
        if my_potential_movements.up in obstacles:
            is_move_safe["up"] = False
        if my_potential_movements.down in obstacles:
            is_move_safe["down"] = False
        if my_potential_movements.right in obstacles:
            is_move_safe["right"] = False
        if my_potential_movements.left in obstacles:
            is_move_safe["left"] = False
        return is_move_safe

    def minimize_distance(my_head: typing.Dict,
                          my_potential_movements: potential_movements,
                          targets: typing.List,
                          move_rating: typing.Dict,
                          board_height: int,
                          board_width: int,
                          weight: float) -> typing.Dict:

        min_distance = board_width*board_height

        for element in targets:
            distance = abs(element['x'] - my_head['x']) +\
                  abs(element['y'] - my_head['y'])
            if distance < min_distance:
                min_distance = distance

        for element in targets:
            potential_distance = abs(element['x'] -
                                     my_potential_movements.up['x']) +\
                                 abs(element['y'] -
                                     my_potential_movements.up['y'])
            if potential_distance < min_distance:
                move_rating['up'] += weight
            potential_distance = abs(element['x'] -
                                     my_potential_movements.down['x']) +\
                                 abs(element['y'] -
                                     my_potential_movements.down['y'])
            if potential_distance < min_distance:
                move_rating['down'] += weight
            potential_distance = abs(element['x'] -
                                     my_potential_movements.right['x']) +\
                                 abs(element['y'] -
                                     my_potential_movements.right['y'])
            if potential_distance < min_distance:
                move_rating['right'] += weight
            potential_distance = abs(element['x'] -
                                     my_potential_movements.left['x']) +\
                                 abs(element['y'] -
                                     my_potential_movements.left['y'])
            if potential_distance < min_distance:
                move_rating['left'] += weight

        return move_rating

    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_id = game_state["you"]["id"]

    my_potential_movements = potential_movements(head=my_head)

    # Step 1 - Prevent your Battlesnake from moving out of bounds
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']
    my_board = board(board_width, board_height)
    walls = my_board.wall

    is_move_safe = check_move(is_move_safe,
                              my_potential_movements,
                              walls)

    # Step 2 - Prevent your Battlesnake from colliding with itself or
    # other Battlesnakes
    all_snakes = snakes(game_state=game_state)
    is_move_safe = check_move(is_move_safe,
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
            enemy_potential_movements = potential_movements(enemy['head'])
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
    dense_tiles = [dict(tpl) for tpl, count in counts.items() if count >= 3]

    move_rating = minimize_distance(my_head,
                                    my_potential_movements,
                                    dense_tiles,
                                    move_rating,
                                    board_height,
                                    board_width,
                                    weight=-0.3)


    # Step 4 - Move towards food instead of random, to regain health and survive longer
    food = game_state['board']['food']
    am_I_hungry = False
    am_I_hunting = False
    length_diff = game_state['you']['length'] - enemy_length

    # weight how hungry you are based on how much larger of a snake you are.
    # If you are way bigger, press your advantage
    if game_state['you']['health'] < 100 - 5*length_diff:
        am_I_hungry = True
    
    if length_diff < 0:
        am_I_hunting = False

    if am_I_hungry:
        move_rating = minimize_distance(my_head,
                                        my_potential_movements,
                                        food,
                                        move_rating,
                                        board_height,
                                        board_width,
                                        weight=0.1)

    if am_I_hunting:
        move_rating = minimize_distance(my_head,
                                        my_potential_movements,
                                        [enemy_head],
                                        move_rating,
                                        board_height,
                                        board_width,
                                        weight=0.1)

    next_move = max(move_rating, key=move_rating.get)

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
