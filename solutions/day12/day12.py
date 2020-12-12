

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


def read_input():
    """Reads the input of the problem and returns it as a list of instructions"""
    instructions = []
    with open('solutions/day12/input.txt') as f:
        for line in f:
            line = line.strip('\n')
            instructions.append(Instruction(line[0], line[1:]))
    return instructions


def rotate_clockwise(waypoint):
    """ Rotates the waypoint 90 degrees clockwise. """
    n = waypoint[0]
    e = waypoint[1]
    return [-e, n]


def rotate_counterclockwise(waypoint):
    """ Rotates the waypoint 90 degrees counter-clockwise. """
    n = waypoint[0]
    e = waypoint[1]
    return [e, -n]


def part1(instructions):
    """ Performs all instructions according to the rules of part 1.
        Returns the manhattan distance from start to end."""
    direction = 'E'
    steps = {'N': 0, 'E': 0, 'S': 0, 'W': 0}
    for i in instructions:
        action = i.action
        if action in ['N', 'E', 'S', 'W']:
            steps[action] += i.value
        elif action == 'F':
            steps[direction] += i.value
        elif action == 'R':
            cur_degrees = cardinal_to_degree[direction] + i.value
            direction = degree_to_cardinal[cur_degrees % 360]
        elif action == 'L':
            cur_degrees = cardinal_to_degree[direction] - i.value
            direction = degree_to_cardinal[cur_degrees % 360]
    return abs(steps['N'] - steps['S']) + abs(steps['E'] - steps['W'])


def part2(instructions):
    """ Performs all instructions according to the rules of part 2.
        Not elegant, but it works.
        Returns the manhattan distance from start to end."""
    waypoint = [1, 10]
    deltas = [0, 0]
    for i in instructions:
        action = i.action
        if action == 'N':
            waypoint[0] += i.value
        elif action == 'E':
            waypoint[1] += i.value
        elif action == 'S':
            waypoint[0] -= i.value
        elif action == 'W':
            waypoint[1] -= i.value
        elif action == 'F':
            deltas[0] += waypoint[0] * i.value
            deltas[1] += waypoint[1] * i.value
        elif action == 'R':
            times = int(i.value / 90)
            for _ in range(times):
                waypoint = rotate_clockwise(waypoint)
        elif action == 'L':
            times = int(i.value / 90)
            for _ in range(times):
                waypoint = rotate_counterclockwise(waypoint)
    return abs(deltas[0]) + abs(deltas[1])


# Find the solutions for part 1 and 2 of the puzzle.
if __name__ == "__main__":
    instructions = read_input()
    print(f"The manhattan distance for part 1: {part1(instructions)}")
    print(f"The manhattan distance for part 2: {part2(instructions)}")
