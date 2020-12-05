import re

MANDATORY = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
OPTIONAL = ['cid']
EYE_COLOURS = ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']


def in_range(x, min, max):
    return int(x) in range(min, max + 1)


def birth_validity(x): return in_range(x, 1920, 2002)
def issue_validity(x): return in_range(x, 2010, 2020)
def expiration_validity(x): return in_range(x, 2020, 2030)
def pid_validity(x): return re.compile(r"^[0-9]{9}$").match(x)
def hair_validity(x): return re.compile(r"^#[0-9a-f]{6}$").match(x)
def height_validity(x): return re.compile(r"^(1[5-8][0-9]|19[0-3])cm|(59|6[0-9]|7[0-6])in$").match(x)
def eye_validity(x): return x in EYE_COLOURS
def country_validity(x): return True


validator_mapping = {
    'byr': birth_validity,
    'iyr': issue_validity,
    'eyr': expiration_validity,
    'hgt': height_validity,
    'hcl': hair_validity,
    'ecl': eye_validity,
    'pid': pid_validity,
    'cid': country_validity
}


def read_input():
    """Reads the input of the problem and stores it as a list of dicts"""
    passports = []
    with open('solutions/day4/input.txt') as f:
        cur_passport = {}
        for line in f:
            if not line.strip():
                passports.append(cur_passport)
                cur_passport = {}
                continue
            else:
                for kv in line.split():
                    k = kv.split(':')[0]
                    v = kv.split(':')[1]
                    cur_passport[k] = v
        passports.append(cur_passport)
    return passports


def check_field_presences(passport):
    """ Checks if all mandatory fields are present in the passport. Oneliner is more for fun than for readability."""
    return set(passport.keys()) in (set(MANDATORY + OPTIONAL), set(MANDATORY))


def check_validity(passport):
    """ Checks if all the needed key value pairs in the passport are present 
        and pass their respective validator tests.
        Oneliner is more for fun than for readability. """
    return check_field_presences(passport) and all(map(lambda kv: validator_mapping[kv[0]](kv[1]), passport.items()))


# Find the solutions for part 1 and 2 of the puzzle.
if __name__ == "__main__":
    passports = read_input()
    # Part 1 - check if all fields are present
    print(len(list(filter(check_field_presences, passports))))
    # Part 2 - check if all fields are present and valid
    print(len(list(filter(check_validity, passports))))
