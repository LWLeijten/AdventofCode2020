from collections import defaultdict
import operator

# https://www.redblobgames.com/grids/hexagons/#coordinates
# Used the cube representation for my hexagonal grid
directions = {
    'ne': (1, 0, -1),
    'nw': (0, 1, -1),
    'se': (0, -1, 1),
    'sw': (-1, 0, 1),
    'e': (1, -1, 0),
    'w': (-1, 1, 0)
}


def read_input():
    """ Reads input file and returns it as a list of tile-directions."""
    tiles = []
    with open(f'solutions/day24/input.txt') as f:
        for line in f:
            tiles.append(line.strip())
    return tiles


def flip_tiles_by_instructions(tiles):
    """ Flips all the tiles as instructed by the set of instructions
        in the tiles parameter. Returns a list of flipped tiles. """
    tile_flips = defaultdict(lambda: 0)
    for tile in tiles:
        pos = (0, 0, 0)
        while len(tile) > 0:
            for d in directions.keys():
                if tile.startswith(d):
                    pos = tuple(map(operator.add, pos, directions[d]))
                    tile = tile.replace(d, "", 1)
                    break
        tile_flips[pos] += 1
    flipped_tiles = list(filter(lambda t: t[1] % 2 == 1, tile_flips.items()))
    return flipped_tiles


def get_neighbours(tile):
    """ Gets the neighbours of a tile on the hexagonal grid. """
    neighbours = []
    for offset in directions.values():
        neighbours.append(tuple(map(operator.add, tile, offset)))
    return neighbours


def get_relevant_tiles(flip_dict):
    """ Creates a set of tiles that we have to check the
        game of life rules against for a given round. """
    blacks = list(flip_dict.keys())
    neighbours = set()
    for b in blacks:
        nbs = get_neighbours(b)
        for nb in nbs:
            neighbours.add(nb)
    targets = blacks + list(neighbours)
    return targets


def simulate_round(flip_dict):
    """ Simulates a round of the game of life.
        First find the target tiles, secondly check them against the decision rules.
        Returns a dict of only flipped tiles after the round is over. """
    targets = get_relevant_tiles(flip_dict)
    output_dict = defaultdict(lambda: 0)
    for t in targets:
        is_black = flip_dict[t]
        black_neighbours = len(
            list(filter(lambda nb: flip_dict[nb] == 1, get_neighbours(t))))
        if is_black and (black_neighbours == 0 or black_neighbours > 2):
            continue
        elif is_black:
            output_dict[t] = 1
        elif not is_black and black_neighbours == 2:
            output_dict[t] = 1
    return output_dict


# Find the solutions for part 1 and 2 of the puzzle.
if __name__ == "__main__":
    tiles = read_input()
    # Part 1
    flips = flip_tiles_by_instructions(tiles)
    # Part 2
    # Init flip_dict from output of part 1
    flip_dict = defaultdict(lambda: 0)
    for f in flips:
        flip_dict[f[0]] = f[1]
    # Simulate 100 rounds
    for i in range(100):
        flip_dict = simulate_round(flip_dict)
        print(f"Done with round {i+1}")

    print(
        f"(Part 1) The amount of flipped tiles after instructions is {len(flips)}")
    print(
        f"(Part 2) The amount of flipped tiles after 100 rounds is {len(flip_dict)}")
