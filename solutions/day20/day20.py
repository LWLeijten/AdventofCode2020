import numpy as np
import math
import re
from functools import reduce
from collections import defaultdict


def read_input():
    """ Reads the input file and returns it as a dict of tiles. """
    with open('solutions/day20/input.txt') as f:
        data = f.read()
    tile_dict = dict()
    tiles_raw = re.split(r'\n\n', data)
    for tile in tiles_raw:
        tile_lines = tile.split('\n')
        tile_id = tile_lines[0][:-1].split()[1]
        tile_dict[int(tile_id)] = np.array([[cell for cell in row]
                                            for row in tile_lines[1:]])
    return tile_dict


def rotate_tile(tile, times):
    """ Rotate a puzzle tile x times. """
    return np.rot90(tile, times)


def flip_tile(tile):
    """ Flip a puzzle tile. """
    return np.fliplr(tile)


def get_top(tile):
    """ Get the top row of a puzzle tile. """
    return str(tile[0, :].tolist())


def get_bottom(tile):
    """ Get the bottom row of a puzzle tile. """
    return str(tile[-1, :].tolist())


def get_left(tile):
    """ Get the leftmost column of a puzzle tile. """
    return str(tile[:, 0].tolist())


def get_right(tile):
    """ Get the rightmost column of a puzzle tile. """
    return str(tile[:, -1].tolist())


def get_borders(tile):
    """ Gets all the unique borders of a puzzle tile. """
    borders = []
    borders.append(get_top(tile))
    borders.append(get_bottom(tile))
    borders.append(get_left(tile))
    borders.append(get_right(tile))
    return list(set(borders))


def tile_permutations(tile):
    """ Returns all permutations (flips, rotations) of a tile. """
    permutations = []
    for i in range(0, 4):
        rotated = rotate_tile(tile, i)
        flipped = flip_tile(rotated)
        permutations.extend([rotated, flipped])
    return permutations


def get_shared_border_count(tile, tile_id, tiles):
    """ Calculates the amount of borders a puzzle tile
        has in common with the other tiles in the puzzle.
        Used to determine the corner tiles with only 2 shared borders. """
    borders = []
    for perm in tile_permutations(tile):
        borders.extend(get_borders(perm))
    borders = set(borders)
    shared_count = 0
    for k, v in tiles.items():
        if k != tile_id:
            for b in get_borders(v):
                if b in borders:
                    shared_count += 1
    return shared_count


def get_overlaps_for_side(side, tile_id, tiles):
    """ For a side of a puzzle tile, calculate the amount of overlaps 
        present in all the other tiles. """
    shared_count = 0
    for k, v in tiles.items():
        if k != tile_id:
            for b in get_borders(v):
                if b == side:
                    shared_count += 1
    return shared_count


def find_corner_pieces(tile_dict):
    """ Find the corner pieces of the jigsaw, by looking for tiles with
        only 2 shared edges. Returns the ids of the 4 corner tiles. """
    corner_ids = []
    for key, tile in tile_dict.items():
        borders = get_shared_border_count(tile, key, tile_dict)
        if borders == 2:
            corner_ids.append(key)
    return corner_ids


def create_image(tile_dict, corner_ids):
    """ Creates the jigsaw puzzle. Starting with a corner piece in the topleft
        and then adding pieces row by row by identifying the common borders of tiles.
        Returns the put together image. """
    used_tiles = set()
    image = defaultdict(lambda: None)
    start_tile = tile_dict[corner_ids[0]]
    used_tiles.add(corner_ids[0])
    # Rotate start-tile to topleft
    while not (get_overlaps_for_side(get_right(start_tile), corner_ids[0], tile_dict) == 1 and
               get_overlaps_for_side(get_bottom(start_tile), corner_ids[0], tile_dict) == 1):
        start_tile = rotate_tile(start_tile, 1)
    image[(0, 0)] = start_tile
    # Put together the puzzle
    for y in range(0, 12):
        for x in range(0, 12):
            if (x, y) == (0, 0):
                continue
            found = False
            left_nb = image[(x-1, y)]
            top_nb = image[(x, y-1)]
            for key, tile in tile_dict.items():
                if key in used_tiles:
                    continue
                elif not found:
                    perms = tile_permutations(tile)
                    for p in perms:
                        if (not isinstance(left_nb, np.ndarray) or get_left(p) == get_right(left_nb)) and (not isinstance(top_nb, np.ndarray) or get_top(p) == get_bottom(top_nb)):
                            found = True
                            used_tiles.add(key)
                            image[(x, y)] = p
                            break
    return image


def trim_image(image_untrimmed):
    """ Trims the borders from the tiles. Each tile starts as a 10*10
        and ends up as a 8*8. Returns the trimmed image."""
    image = np.empty(shape=(96, 96), dtype=str)
    for y in range(12):
        for x in range(12):
            image[y*8:(y+1)*8, x*8:(x+1) *
                  8] = image_untrimmed[(x, y)][1:-1, 1:-1]
    return image


def find_monsters(image):
    """ Given the trimmed image, finds the monsters in the image.
        Returns the amount of rough water spaces in which there is
        no monster present. """
    monster = np.array((
        list("                  # "),
        list("#    ##    ##    ###"),
        list(" #  #  #  #  #  #   ")
    ))
    monster_indices = {(x, y) for y, x in zip(*np.where(monster == "#"))}
    (monster_height, monster_width) = monster.shape
    (image_width, image_height) = image.shape
    monsters = 0
    attempt = 1
    while monsters == 0:
        for y in range(image_height - monster_height + 1):
            for x in range(image_width - monster_width + 1):
                coords = list(map(lambda xy: (
                    xy[0] + x, xy[1] + y), monster_indices))
                if all(list(map(lambda c: image[c[0]][c[1]] == '#', coords))):
                    monsters += 1
        if monsters == 0:
            if attempt == 4:
                image = rotate_tile(image, 1)
                image = flip_tile(image)
            else:
                image = rotate_tile(image, 1)
            attempt += 1
    rough_waters = np.count_nonzero(image == '#')
    rough_waters = rough_waters - monsters * len(monster_indices)
    return rough_waters


# Find the solutions for part 1 and 2 of the puzzle.
if __name__ == "__main__":
    tile_dict = read_input()
    # Part 1
    corner_ids = find_corner_pieces(tile_dict)
    print(
        f"The product of corner ids is: {reduce((lambda x, y: x * y), corner_ids)}")
    # Part 2
    image = create_image(tile_dict, corner_ids)
    image = trim_image(image)
    rough_waters = find_monsters(image)
    print(f"Amount of rough water tiles without monsters is {rough_waters}")
