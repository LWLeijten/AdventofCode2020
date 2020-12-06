
def read_input():
    """Reads the input of the problem and returns it as a list of groups with question numbers"""
    groups = []
    with open('solutions/day6/input.txt') as f:
        cur_group = []
        people = 0
        for line in f:
            if not line.strip():
                groups.append((cur_group, people))
                cur_group = []
                people = 0
            else:
                people += 1
                for char in line.strip('\n'):
                    cur_group.append(char)
        groups.append((cur_group, people))
    return groups


def count_anyone(groups):
    """ Counts the questions for which ANYONE in the group gave yes as an answer."""
    return sum(map(lambda g: len(set(g[0])), groups))


def count_everyone(groups):
    """ Counts the questions for which EVERYONE in the group gave yes as an answer."""
    return sum(map(lambda g: len(list(filter(lambda a: g[0].count(a) == g[1], set(g[0])))), groups))


# Find the solutions for part 1 and 2 of the puzzle.
if __name__ == "__main__":
    groups = read_input()
    print(count_anyone(groups))
    print(count_everyone(groups))


""" 
Since the one-liners might be more for fun and challenge than human readability,
below are count_anyone() and count_everyone() defined in a more human-friendly way

def count_anyone():
    count = 0
    for (answers, _) in groups:
        count += len(set(answers))
    return count

def count_everyone():
    count = 0
    for (answers, people) in groups:
        questions = set(answers)
        for q in questions:
            count += (answers.count(q) == people)
    return count 
    
"""
