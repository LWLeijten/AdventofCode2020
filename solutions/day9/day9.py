from itertools import combinations


def read_input():
    """Reads the input of the problem and returns it as a numbers list"""
    numbers = []
    with open('solutions/day9/input.txt') as f:
        for line in f:
            numbers.append(int(line.strip(' \n')))
    return numbers


def find_target(numbers):
    """ Finds the first number after te preamble for which
        there is no combination of 2 numbers before it in the list
        that sum towards that number."""
    for i, num in enumerate(numbers):
        if i >= 25 and not any([a + b == num for a, b in combinations(numbers[i-25:i], 2)]):
            return num


def find_weakness(numbers, target):
    """ Finds a contiguous set in the list of numbers
        that summed together are equal to the target.
        Returns the sum of the lowest and highest number in this set."""
    for lower_bound in range(len(numbers)):
        upper_bound = lower_bound
        set_sum = 0
        while set_sum < target:
            set_sum = sum(numbers[lower_bound:upper_bound])
            upper_bound += 1
        if set_sum == target:
            sublist = numbers[lower_bound:upper_bound]
            return min(sublist) + max(sublist)


# Find the solutions for part 1 and 2 of the puzzle.
if __name__ == "__main__":
    numbers = read_input()
    # part 1
    target = find_target(numbers)
    print(f"The target number is: {target}")
    # part 2
    print(f"The encrpytion weakness is: {find_weakness(numbers, target)}")
