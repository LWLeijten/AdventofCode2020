
def transform(value, subject):
    """ Transforms a number according to the problem description. """
    return (value * subject) % 20201227


def calc_loop_size(public, subject):
    """ Calculates loop size by transforming the with
        given subject number untill it is equal to the public key."""
    value = 1
    loops = 0
    while value != public:
        value = transform(value, subject)
        loops += 1
    return loops


def calc_encryption_key(public, loop_size):
    """ Calculates encryption key by transforming using
        the public key as subject and the found loop_size. """
    value = 1
    for _ in range(loop_size):
        value = transform(value, public)
    return value

    # Find the solutions for part 1 and 2 of the puzzle.
if __name__ == "__main__":
    subject = 7
    card_public = 1717001
    door_public = 523731
    card_loop_size = calc_loop_size(card_public, subject)
    door_loop_size = calc_loop_size(door_public, subject)
    encryption_key = calc_encryption_key(card_public, door_loop_size)
    encryption_key2 = calc_encryption_key(door_public, card_loop_size)
    print(f"The encryption key is {encryption_key}")
    print(f"The encryption key is {encryption_key2}")
