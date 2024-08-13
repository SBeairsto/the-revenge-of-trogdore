from typing import List, Dict, Tuple
import snake_classes
from snake_classes import potential_movements

def check_move(is_move_safe: Dict,
                   my_potential_movements: potential_movements,
                   obstacles: Dict) -> Dict:
        if my_potential_movements.up in obstacles:
            is_move_safe["up"] = False
        if my_potential_movements.down in obstacles:
            is_move_safe["down"] = False
        if my_potential_movements.right in obstacles:
            is_move_safe["right"] = False
        if my_potential_movements.left in obstacles:
            is_move_safe["left"] = False
        return is_move_safe


def minimize_distance(my_head: Dict,
                          my_potential_movements: potential_movements,
                          targets: List,
                          move_rating: Dict,
                          board_height: int,
                          board_width: int,
                          max_dist: int,
                          weight: float) -> Dict:

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


def avoid_bigger_snakes(move_rating: Dict,
                        game_state: Dict,
                        moves: List,
                        my_id: str,
                        my_potential_movements: potential_movements,
                        ) -> Tuple[Dict, int, List]:
    for enemy in game_state['board']['snakes']:
        if enemy['id'] != my_id:
            enemy_potential_movements = snake_classes.potential_movements(enemy['head'])
            enemy_length = enemy['length']
            enemy_head = enemy['head']
            if enemy['length'] >= game_state['you']['length']:
                for move in moves:
                    if getattr(my_potential_movements, move) in enemy_potential_movements.all:
                        move_rating[move] -= 0.5
    return move_rating, enemy_length, enemy_head


def add_adjacent_positions(element: Dict[str, str],
                           collection: List[Dict[str, int]]):
    collection.extend([
        {'x': element['x'] + 1, 'y': element['y']},
        {'x': element['x'] - 1, 'y': element['y']},
        {'x': element['x'], 'y': element['y'] + 1},
        {'x': element['x'], 'y': element['y'] - 1}
    ])


def remove_matching_dicts(A: List[Dict[str, int]], B: List[Dict[str, int]]) -> List[Dict[str, int]]:
    # Convert list B to a set of frozensets for efficient lookup
    set_B = {frozenset(d.items()) for d in B}
    
    # Filter out dictionaries in A that match any dictionary in B
    filtered_A = [d for d in A if frozenset(d.items()) not in set_B]
    
    return filtered_A
