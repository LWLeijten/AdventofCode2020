def play_game(numbers, rounds):
    memory = {}
    for i, n in enumerate(numbers):
        memory[n] = [i]
    while len(numbers) < rounds:
        cur_index = len(numbers) - 1
        last_num = numbers[cur_index]
        if len(memory[last_num]) == 1:
            numbers.append(0)
            if 0 not in memory:
                memory[0] = [cur_index + 1]
            else:
                memory[0].append(cur_index + 1)
                memory[0] = memory[0][-2:]
        else:
            new_num = memory[last_num][-1] - memory[last_num][-2]
            numbers.append(new_num)
            if new_num not in memory:
                memory[new_num] = [cur_index + 1]
            else:
                memory[new_num].append(cur_index+1)
            if len(memory[new_num]) > 2:
                memory[new_num] = memory[new_num][-2:]
    return numbers[rounds-1]


# Find the solutions for part 1 and 2 of the puzzle.
if __name__ == "__main__":
    numbers = [9, 12, 1, 4, 17, 0, 18]
    print(play_game(numbers, 2020))
    print(play_game(numbers, 30000000))
