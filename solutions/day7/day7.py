import networkx as nx
import re


def read_input():
    hash_table = {}
    hash_table2 = {}
    parent_regex = re.compile(r"^(\w+ \w+)")
    child_regex = re.compile(r"(\d+) (\w+ \w+)")
    with open('solutions/day7/input.txt') as f:
        for line in f:
            parent = parent_regex.match(line).group(1)
            hash_table2[parent] = []
            children = child_regex.findall(line)
            if children:
                for child in children:
                    hash_table2[parent].append((child[1], child[0]))
                    if not child[1] in hash_table.keys():
                        hash_table[child[1]] = [(parent, child[0])]
                    else:
                        hash_table[child[1]].append((parent, child[0]))
    return hash_table, hash_table2


result_set = set()


def gold_possibilities(hash_table, root):
    if not root in hash_table.keys():
        result_set.add(root)
    else:
        for tup in hash_table[root]:
            result_set.add(tup[0])
            gold_possibilities(hash_table, tup[0])
    return result_set


def count_content(ht, root):
    total = 1
    for tup in ht[root]:
        total += (int(tup[1]) * count_content(ht, tup[0]))
    return total


hash_table, hash_table2 = read_input()
gold_possibilities(hash_table, 'shiny gold')
print(len(result_set))
# minus 1 for the shiny gold bag itself
print(count_content(hash_table2, 'shiny gold') - 1)
