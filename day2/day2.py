from operator import xor


class PasswordProblem():
    """ Class holding all the variables for one line of the puzzle """

    def __init__(self, password, letter, low, high):
        self.password = password
        self.letter = letter
        self.low = low
        self.high = high


def read_input():
    """Reads the input of the problem"""
    passwords = []
    with open('day2/day2Input.txt') as f:
        for line in f:
            num_range, letter, password = line.split(' ')
            low, high = num_range.split('-')
            passwords.append(PasswordProblem(
                password, letter[0], int(low), int(high)))
    return passwords


def valid_password_part_1(p: PasswordProblem):
    """Given a problem instance, checks whether the designated letter apears a valid amount of times."""
    count = p.password.count(p.letter)
    return count >= p.low and count <= p.high


def valid_password_part_2(p: PasswordProblem):
    """Given a problem instance, checks whether the designated letter apears in exactly of the two given positions."""
    target = p.letter
    letter1 = p.password[p.low - 1]
    letter2 = p.password[p.high - 1]
    return xor(target == letter1, target == letter2)


# Find the solutions for part 1 and 2 of the puzzle.
if __name__ == "__main__":
    passwords = read_input()
    print(len(list((filter(valid_password_part_1, passwords)))))
    print(len(list((filter(valid_password_part_2, passwords)))))
