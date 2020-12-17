import re
from itertools import combinations, permutations


class Rule():
    """ Class for a rule. Holds its name and the set of valid ranges for this rule. """

    def __init__(self, name, ranges):
        self.name = name
        self.ranges = ranges

    def validate_number(self, number):
        """ Validates a number against this specific rule. """
        return any([number >= int(r[0]) and number <= int(r[1]) for r in self.ranges])


def read_input():
    """ Reads the input and returns it as a list of rules, a list of tickets and our own ticket.
        Definitely not pretty but it gets the job done."""
    rules = []
    tickets = []
    my_ticket = []
    reading_mine = False
    reading_others = False
    with open('solutions/day16/input.txt') as f:
        for line in f:
            if not line == '\n':
                if not (line.startswith('your ticket') or line.startswith('nearby tickets')) and not reading_mine and not reading_others:
                    name_regex = re.compile(r"^(\w+ )*(\w+):")
                    range_regex = re.compile(r"\d+-\d+")
                    name = name_regex.match(line).group(0)
                    ranges = range_regex.findall(line)
                    ranges_tups = [(r.split('-')[0], r.split('-')[1])
                                   for r in ranges]
                    rules.append(Rule(name, ranges_tups))
                elif line.startswith('your ticket'):
                    reading_mine = True
                elif reading_mine:
                    my_ticket = line.split(',')
                    reading_mine = False
                elif line.startswith('nearby tickets'):
                    reading_others = True
                elif reading_others:
                    tickets.append(line.split(','))
    return rules, tickets, my_ticket


def validate_tickets(rules, tickets):
    """ Validates the list of tickets to the given rules.
        Returns the list of valid tickets and the error rate. """
    valid_tickets = []
    faults = 0
    for t in tickets:
        invalid = False
        for num in t:
            if not any([r.validate_number(int(num)) for r in rules]):
                faults += int(num)
                invalid = True
        if not invalid:
            valid_tickets.append(t)
    return valid_tickets, faults


def setup_possibilities(rules):
    """ Sets up a dictionary holding the possible indices
        for each of the rules in our ruleset. """
    possibilities = dict()
    for r in rules:
        possibilities[r.name] = [i for i in range(len(rules))]
    return possibilities


def remove_out_of_range(possibilities, rules, tickets):
    """ Given the possibilities dict, the rules and tickets,
        removes the rules for positions in which values exist 
        that lay outside the valid range. Returns the smaller possibilities dict. """
    for t in tickets:
        for i, num in enumerate(t):
            for rule in rules:
                if not rule.validate_number(int(num)) and i in possibilities[rule.name]:
                    possibilities[rule.name].remove(i)
    return possibilities


def solve_by_eliminating(possibilities):
    """ Finds the positions of all rules by elimination.
        The algorithm looks for any rules that have only one possibilities (ergo its locked)
        and removes that index for all other rules in the possibilities dict untill all rules
        remain with 1 viable position. """
    while not all(len(v) == 1 for k, v in possibilities.items()):
        singular_rules = list(
            filter(lambda kv: len(kv[1]) == 1, possibilities.items()))
        for sr in singular_rules:
            number = sr[1][0]
            for k, v in possibilities.items():
                if number in v and not k == sr[0]:
                    v.remove(number)
    return possibilities


def determine_rule_order(rules, tickets):
    """ Determines the rule order given a set of rules and a list of tickets.
        First it removes all possibilities that are always illegal (out of bounds numbers).
        Next it solves the problem by eliminating, starting at rules that only have 1 possibility and removing
        that from the other possibilities, untill all rules have 1 position left.
        Returns the product of values for all departure-based rules in our own ticket. """
    possibilities = setup_possibilities(rules)
    possibilities = remove_out_of_range(possibilities, rules, tickets)
    possibilities = solve_by_eliminating(possibilities)
    departures = list(
        filter(lambda kv: kv[0].startswith('departure'), possibilities.items()))
    result = 1
    for tup in departures:
        result *= int(my_ticket[tup[1][0]])
    return result


# Find the solutions for part 1 and 2 of the puzzle.
if __name__ == "__main__":
    rules, tickets, my_ticket = read_input()
    # Part 1
    valid_tickets, error_rate = validate_tickets(rules, tickets)
    print(f"The error rate in the tickets is {error_rate}")
    # Part 2
    departure_product = determine_rule_order(rules, valid_tickets)
    print(f"The product of departure fields is {departure_product}")
