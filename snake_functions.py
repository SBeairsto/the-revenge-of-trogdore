import typing
from snake_classes import potential_movements

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
                          max_dist: int,
                          weight: float) -> typing.Dict:

    min_distance = board_width*board_height
    if min_distance > max_dist:
        return move_rating, min_distance

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

    return move_rating, min_distance