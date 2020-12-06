
def read_input():
    """Reads the input of the problem and returns it as a list of sets of yes answers"""
    groups = []
    cur_group = []
    with open('solutions/day6/input.txt') as f:
        for line in f:
            if not line.strip():
                groups.append(cur_group)
                cur_group = []
            else:
                cur_person = []
                for char in line.strip('\n'):
                    cur_person.append(char)
                cur_group.append(set(cur_person))
        groups.append(cur_group)
    return groups


def count_anyone(groups):
    """ Counts the questions for which ANYONE in the group gave yes as an answer."""
    return sum([len(set.union(*g)) for g in groups])


def count_everyone(groups):
    """ Counts the questions for which EVERYONE in the group gave yes as an answer."""
    return sum([len(set.intersection(*g)) for g in groups])


# Find the solutions for part 1 and 2 of the puzzle.
if __name__ == "__main__":
    groups = read_input()
    print(count_anyone(groups))
    print(count_everyone(groups))
