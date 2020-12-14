from itertools import product


def split_line(line):
    """ Processes a line into the memory slot and the to assign number."""
    number = line.split('=')[1]
    memory_slot = line.split('=')[0][4:-1]
    return memory_slot, number


def to_36bit_string(input):
    """ Transforms a number into a 0-padded 36 bits string."""
    bits = f'{int(input):36b}'
    bits = ('{:036d}'.format(int(bits)))
    return bits


def bitlist_to_numerical(bitlist):
    """ Transforms a list of bits into an integer."""
    return int(''.join(bitlist), 2)


def fill_floating_bits(bitstring):
    """ Generates all the resulting bitstrings when filling in
        the floating bits with either a 0 or 1."""
    addresses = []
    indices = [i for i, c in enumerate(bitstring) if c == 'X']
    bitlist = list(bitstring)
    for t in product('01', repeat=len(indices)):
        for i, c in zip(indices, t):
            bitlist[i] = c
        numerical = bitlist_to_numerical(bitlist)
        addresses.append(numerical)
    return addresses


def version_1_decoding():
    """ Processes the input according to the rules of part 1.
        Using the mask to overwrite bits before writing to memory."""
    mask = ""
    memory = dict()
    with open('solutions/day14/input.txt') as f:
        for line in f:
            line = line.replace(' ', '').strip()
            if line.startswith('mask'):
                mask = line.split('=')[1]
            else:
                memory_slot, number = split_line(line)
                bitlist = list(to_36bit_string(number))
                for i, bit in enumerate(mask):
                    if bit != 'X':
                        bitlist[i] = bit
                memory[memory_slot] = bitlist_to_numerical(bitlist)
    return memory


def version_2_decoding():
    """ Processes the input according to the rules of part 2.
        Calculates all permutations of the floating bits and writes the result
        to all the different memory locations generated this way. """
    mask = ""
    memory = dict()
    with open('solutions/day14/input.txt') as f:
        for line in f:
            line = line.replace(' ', '').strip()
            if line.startswith('mask'):
                mask = line.split('=')[1]
            else:
                memory_slot, number = split_line(line)
                memory_bits = list(to_36bit_string(memory_slot))
                for i, bit in enumerate(mask):
                    if bit in ['1', 'X']:
                        memory_bits[i] = bit
                addresses = fill_floating_bits(memory_bits)
                for address in addresses:
                    memory[address] = number
    return memory


# Find the solutions for part 1 and 2 of the puzzle.
if __name__ == "__main__":
    # Part 1
    memory1 = version_1_decoding()
    print(sum(memory1.values()))
    # Part 2
    memory2 = version_2_decoding()
    print(sum(map(lambda m: int(m), memory2.values())))
