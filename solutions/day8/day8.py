from copy import copy
import operator

ops = {
    '+': operator.add,
    '-': operator.sub
}


class Instruction():
    def __init__(self, operation, argument):
        self.operation = operation
        self.argument = argument

    def arg_op(self):
        return self.argument[0]

    def arg_val(self):
        return int(self.argument[1:])


def read_input():
    """ Read the input and return it as an ordered list of Instructions."""
    instructions = []
    with open('solutions/day8/input.txt') as f:
        for line in f:
            splits = line.split()
            instructions.append(Instruction(splits[0], splits[1]))
    return instructions


def perform_instruction(instruction, pnt, acc):
    """ Performs an instruction for a state with pointer and accumulator.
        Returns the resulting pointer and accumulator. """
    if instruction.operation == 'nop':
        pnt += 1
    elif instruction.operation == 'acc':
        pnt += 1
        acc = ops[instruction.arg_op()](acc, instruction.arg_val())
    elif instruction.operation == 'jmp':
        pnt = ops[instruction.arg_op()](pnt, instruction.arg_val())
    return pnt, acc


def execute_program(instructions):
    """ Executes a list of instructions as a program.
        Exit conditions are finding a loop and finishing a succesful execution.
        Returns the resulting accumulator value and a success status. """
    visited = set()
    pnt = acc = 0
    while not instructions[pnt] in visited:
        instruction = instructions[pnt]
        visited.add(instruction)
        pnt, acc = perform_instruction(instruction, pnt, acc)
        if pnt >= len(instructions):
            return acc, True
    return acc, False


def brute_force(instructions):
    """ Swaps all the nops for jmps and vice versa in a brute force manner.
        Keeps bruteforcing permutations untill a succesful execution is found.
        Returns the accumulator and success status of a succesful execution. """
    for i, instruction in enumerate(instructions):
        if instruction.operation != 'acc':
            instructions_copy = copy(instructions)
            if instruction.operation == 'nop':
                instructions_copy[i] = Instruction('jmp', instruction.argument)
            elif instruction.operation == 'jmp':
                instructions_copy[i] = Instruction('nop', instruction.argument)
            accum, success = execute_program(instructions_copy)
            if success:
                return accum, success


instructions = read_input()
# part 1
print(execute_program(instructions))
# part 2 brute forcing
print(brute_force(instructions))
