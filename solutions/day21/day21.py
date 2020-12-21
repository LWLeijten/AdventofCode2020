from collections import defaultdict
import re

INGR_REGEX = re.compile(r"^(\w+ )+")
ALLRG_REGEX = re.compile(r"\(contains (.*?)\)")


def read_input():
    """ Reads the input and processes it. Returns a dictionary
        containing for each allergent its possible ingredients causing it and
        a dictionary of all ingredients and its occurence count."""
    allergy_possibilities = dict()
    ingredients_dict = defaultdict(lambda: 0)
    with open(f'solutions/day21/input.txt') as f:
        for line in f:
            # Split the line into the ingredients and allergents using regex.
            line = line.strip()
            ingredients = INGR_REGEX.match(line).group(0).split()
            allergents = "".join(ALLRG_REGEX.search(
                line).group(1).split()).split(',')

            # Update the occurence counts of all ingredients.
            for i in ingredients:
                ingredients_dict[i] += 1

            # Keep track of what ingredients could cause what allergy.
            # Do so by using set intersection with previous lines of that allergy.
            for a in allergents:
                if not a in allergy_possibilities:
                    allergy_possibilities[a] = set(ingredients)
                else:
                    allergy_possibilities[a] = allergy_possibilities[a].intersection(
                        set(ingredients))
    return allergy_possibilities, ingredients_dict


def solve_by_elimination(allergies):
    """ Same code used to eliminate tickets on day 16. 
        Finds the ingredient/allergent combinations by elimination.
        The algorithm looks for any allergents that have only one possibilities (ergo its locked)
        and removes that ingredient for all other allergents in the possibilities dict untill all allergents
        remain with 1 viable ingredient causing it.
    """
    while not all(len(v) == 1 for k, v in allergies.items()):
        singles = list(filter(lambda kv: len(kv[1]) == 1, allergies.items()))
        for sr in singles:
            ingr = list(sr[1])[0]
            for k, v in allergies.items():
                if ingr in v and not k == sr[0]:
                    v.remove(ingr)
    return allergies


def find_safe_ingredients(allergies, ingredients_dict):
    """ Returns the amount of occurences of safe ingredients. """
    all_possible_allergents = allergies.values()
    ingredients = set()
    # Unpack all the ingredients in the allergies dict
    for l in all_possible_allergents:
        for elem in l:
            ingredients.add(elem)
    ingredients = list(ingredients)
    # Count the occurences of ingredients not in any allergy list
    count = 0
    for k, v in ingredients_dict.items():
        if k not in ingredients:
            count += int(v)
    return count


# Find the solutions for part 1 and 2 of the puzzle.
if __name__ == "__main__":
    # Part 1
    allergies, ingredients_dict = read_input()
    safe_ingredient_count = find_safe_ingredients(allergies, ingredients_dict)
    print(f"Allergy-prove ingredients appear {safe_ingredient_count} times.")

    # Part 2
    allergies = solve_by_elimination(allergies)
    result = [list(allergies[a])[0] for a in sorted(allergies.keys())]
    print(f"The canonical dangerous ingriedent list is {','.join(result)}")
