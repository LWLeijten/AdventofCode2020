

class Instruction():
    """ An instruction consisting of an action and value. """

    def __init__(self, action, value):
        self.action = action
        self.value = int(value)


""" Mapping from degrees to cardinal direction. """
degree_to_cardinal = {
    0: 'N',
    90: 'E',
    180: 'S',
    270: 'W'
}

""" Mapping from cardinal direction to degrees. """
cardinal_to_degree = {
    'N': 0,
    'E': 90,
    'S': 180,
    'W': 270
}

""" Movement deltas for each of the cardinal directions. """
directions = {
    'N': (0, 1),
    'E': (1, 0),
    'S': (0, -1),
    'W': (-1, 0)
}


def read_input():
    """Reads the input of the problem and returns it as a list of instructions"""
    instructions = []
    with open('solutions/day12/input.txt') as f:
        for line in f:
            line = line.strip('\n')
            instructions.append(Instruction(line[0], line[1:]))
    return instructions


def rotate_clockwise(waypointx, waypointy):
    """ Rotates the waypoint 90 degrees clockwise. """
    return waypointy, -waypointx


def rotate_counterclockwise(waypointx, waypointy):
    """ Rotates the waypoint 90 degrees counter-clockwise. """
    return -waypointy, waypointx


def rotate_waypoint(wptx, wpty, direction, degrees):
    """ Rotates the waypoints current positions into the given direction
        by the given amount of degrees. """
    times = int(degrees / 90)
    if direction == 'L':
        rotate_function = rotate_counterclockwise
    elif direction == 'R':
        rotate_function = rotate_clockwise
    for _ in range(times):
        wptx, wpty = rotate_function(wptx, wpty)
    return wptx, wpty


def move_obj(x, y, direction, amount):
    """ Moves an object from current x and y
        to a new x y given by the direction and amount of movement.
        Returns the new position of the object."""
    x += directions[direction][0] * amount
    y += directions[direction][1] * amount
    return x, y


def rotate_boat(facing, direction, degrees):
    """ Rotates the boat given its current facing, the direction of rotation
        and the degrees of rotation. Returns the new facing."""
    if direction == 'R':
        cur_degrees = cardinal_to_degree[facing] + degrees
    elif direction == 'L':
        cur_degrees = cardinal_to_degree[facing] - degrees
    return degree_to_cardinal[cur_degrees % 360]


def part1(instructions):
    """ Performs all instructions according to the rules of part 1.
        Returns the manhattan distance from start to end."""
    facing = 'E'
    x_pos = y_pos = 0
    for i in instructions:
        action = i.action
        if action in ['N', 'E', 'S', 'W']:
            x_pos, y_pos = move_obj(x_pos, y_pos, action, i.value)
        elif action == 'F':
            x_pos, y_pos = move_obj(x_pos, y_pos, facing, i.value)
        elif action in ['R', 'L']:
            facing = rotate_boat(facing, action, i.value)
    return abs(x_pos) + abs(y_pos)


def part2(instructions):
    """ Performs all instructions according to the rules of part 2.
        Not elegant, but it works.
        Returns the manhattan distance from start to end."""
    wptx = 10
    wpty = 1
    x_pos = y_pos = 0
    for i in instructions:
        action = i.action
        if action in ['N', 'E', 'S', 'W']:
            wptx, wpty = move_obj(wptx, wpty, action, i.value)
        elif action == 'F':
            x_pos += wptx * i.value
            y_pos += wpty * i.value
        elif action in ['R', 'L']:
            wptx, wpty = rotate_waypoint(wptx, wpty, action, i.value)
    return abs(x_pos) + abs(y_pos)


# Find the solutions for part 1 and 2 of the puzzle.
if __name__ == "__main__":
    instructions = read_input()
    print(f"The manhattan distance for part 1: {part1(instructions)}")
    print(f"The manhattan distance for part 2: {part2(instructions)}")
