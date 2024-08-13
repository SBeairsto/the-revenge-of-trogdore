import typing


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
                self.density.append({'x': i, 'y': j, 'd': 0})

        self.corners = [{'x': 0, 'y': 0},
                        {'x': 0, 'y': board_height-1},
                        {'x': board_width-1, 'y': 0},
                        {'x': board_width-1, 'y': board_height-1}]
