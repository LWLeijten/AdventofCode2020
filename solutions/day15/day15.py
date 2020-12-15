def play_game(numbers, rounds):
    """ Plays the memory with a given startlist of numbers for a certain amount of rounds.
        Use a dictionary to keep track of the last occurences of numbers for efficiency. """

    # Init memory with the starting numbers
    memory = {}
    for i, n in enumerate(numbers):
        memory[n] = i

    # Play the game for the given amount of rounds
    while len(numbers) < rounds:
        cur_index = len(numbers) - 1
        last_num = numbers[cur_index]
        if last_num not in memory:
            numbers.append(0)
            memory[last_num] = cur_index
        else:
            numbers.append(cur_index - memory[last_num])
            memory[last_num] = cur_index
    return numbers[rounds-1]


# Find the solutions for part 1 and 2 of the puzzle.
if __name__ == "__main__":
    numbers = [9, 12, 1, 4, 17, 0, 18]
    print(play_game(numbers, 2020))
    print(play_game(numbers, 30000000))
