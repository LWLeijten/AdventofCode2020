from lark import Lark
import re


def read_grammar(filename):
    """ Reads a grammar input file and returns it as a lark grammar."""
    grammar = []
    with open(f'solutions/day19/{filename}') as f:
        for line in f:
            # Since lark cannot handle digits as rule id's, replace each digit by rule{digit}
            rule = re.sub(r'(\d+)', r'rule\1', line.strip())
            grammar.append(rule)
    grammar = "\n".join(grammar)
    return Lark(grammar, start="rule0")


def read_sentences():
    """ Reads the sentences input file and returns it as a list of sentences. """
    sentences = []
    with open('solutions/day19/sentences.txt') as f:
        for line in f:
            sentences.append(line.strip())
    return sentences


def try_parse(sentence, grammar):
    """ Tries to parse a sentence with the given grammar.
        Returns a success value. """
    try:
        grammar.parse(sentence)
        return True
    except:
        return False


# Find the solutions for part 1 and 2 of the puzzle.
if __name__ == "__main__":
    sentences = read_sentences()
    grammar1 = read_grammar('grammar_part1.txt')
    grammar2 = read_grammar('grammar_part2.txt')

    # Part 1
    successes1 = sum([1 for s in sentences if try_parse(s, grammar1)])
    print(successes1)

    # Part 2
    successes2 = sum([1 for s in sentences if try_parse(s, grammar2)])
    print(successes2)
