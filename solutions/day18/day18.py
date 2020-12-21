import operator
import re


ops = {
    '+': operator.add,
    '*': operator.mul
}


def read_input():
    """ Reads the input file and returns it as a list of equations. """
    with open('solutions/day18/input.txt') as f:
        equations = ["".join(e.split()) for e in f]
        return equations


def find_inner_expression(equation):
    """ Returns the indices of the innermost pair of parentheses. """
    stack = []
    if not '(' in equation:
        return False
    for i, c in enumerate(equation):
        if c == '(':
            stack.append(i)
        elif c == ')':
            start = stack.pop()
            return start, i


def evaluate_with_regex(expression, regex):
    """ Evaluates an expression according to a given regex.
        In practice this regex produces either a sum or a mult."""
    while regex.search(expression):
        match = regex.search(expression)
        num1 = int(match.group(1))
        op = match.group(2)
        num2 = int(match.group(3))
        expression = re.sub(regex, str(
            ops[op](num1, num2)), expression, count=1)
    return expression


def evaluate_sums(expression):
    """ Evaluates all the sums (a+b) within an expression.
        Used in the precedence part of the problem. """
    sum_regex = re.compile(r"(\d+)(\+)(\d+)")
    return evaluate_with_regex(expression, sum_regex)


def evaluate_mults(expression):
    """ Evaluates all the mults (a*b) within an expression.
        Used in the precedence part of the problem. """
    mul_regex = re.compile(r"(\d+)(\*)(\d+)")
    return evaluate_with_regex(expression, mul_regex)


def evaluate_with_precedence(expression):
    """ Evaluates an expression using the given precedence.
        First solve all the sums then solve all the mults. """
    expression = evaluate_sums(expression)
    expression = evaluate_mults(expression)
    return expression


def evaluate_left_to_right(expression):
    """ Evaluates an expression reading from left to right.
        Used for the first solution. """
    exp_regex = re.compile(r"^(\d+)([\*\+])(\d+)")
    return evaluate_with_regex(expression, exp_regex)


def solve_equation(equation, precedence=False):
    """ Solves an equation. Finds the innermost set of parentheses and 
        solves the expression within, untill no parentheses are left and the 
        final expression can be evaluated. Optional parameter turns precedence on or off. """
    while find_inner_expression(equation):
        start, end = find_inner_expression(equation)
        if precedence:
            result = evaluate_with_precedence(equation[start+1:end])
        else:
            result = evaluate_left_to_right(equation[start+1:end])
        equation = equation[:start] + result + equation[end+1:]
    if precedence:
        equation = evaluate_with_precedence(equation)
    else:
        equation = evaluate_left_to_right(equation)
    return equation


# Find the solutions for part 1 and 2 of the puzzle.
if __name__ == "__main__":
    equations = read_input()
    # Part 1
    result = sum(map(lambda e: int(solve_equation(e)), equations))
    print(result)
    # Part 2
    result2 = sum(map(lambda e: int(solve_equation(e, True)), equations))
    print(result2)
