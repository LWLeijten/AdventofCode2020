from functools import reduce


def read_input():
    """Reads the input of the problem and stores it as a 2d matrix"""
    grid = []
    with open('day3/input.txt') as f:
        for i, line in enumerate(f):
            grid.append([])
            for char in line.strip('\n'):
                grid[i].append(char)
    return grid


def traverse_grid(grid, x_step, y_step):
    """Traverses a given grid with variable x_step and y_step.
       Use modulo to wrap the grid horizontally"""
    cur_x, cur_y, trees = 0, 0, 0
    while cur_y < len(grid) - 1:
        cur_x = (cur_x + x_step) % len(grid[0])
        cur_y += y_step
        trees += grid[cur_y][cur_x] == '#'
    return trees


# Find the solutions for part 1 and 2 of the puzzle.
if __name__ == "__main__":
    grid = read_input()
    # Part 1
    print(traverse_grid(grid, 3, 1))
    # Part 2
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    results = []
    for x_step, y_step in slopes:
        results.append(traverse_grid(grid, x_step, y_step))
    print(reduce((lambda a, b: a * b), results))
