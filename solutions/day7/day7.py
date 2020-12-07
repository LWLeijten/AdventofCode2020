import networkx as nx
import re


def read_input():
    """ Construct a directed graph of all the bags.
        An edge represents a parent bag containing X amount of bags of the child."""
    DG = nx.DiGraph()
    parent_regex = re.compile(r"^(\w+ \w+)")
    child_regex = re.compile(r"(\d+) (\w+ \w+)")
    with open('solutions/day7/input.txt') as f:
        for line in f:
            parent = parent_regex.match(line).group(1)
            children = child_regex.findall(line)
            if not parent in DG:
                DG.add_node(parent)
            if children:
                for child in children:
                    if not child[1] in DG:
                        DG.add_node(child[1])
                    DG.add_edge(parent, child[1], distance=int(child[0]))
    return DG


def gold_possibilities(graph, cur_node, visited=set()):
    """ Recursively traverses the graph from the target node upward.
        Keeps track of a set of visited nodes to determine the final count. """
    for pred in graph.predecessors(cur_node):
        visited.add(pred)
        gold_possibilities(graph, pred, visited)
    return len(visited)


def count_content(graph, cur_node):
    """ Recursively traverses the graph from the target node downward.
        Counts the amount of child bags in order to form a final total. """
    total = 1
    for succ in graph.successors(cur_node):
        edge = graph.edges[cur_node, succ]
        total += edge.get('distance') * count_content(graph, succ)
    return total


# Find the solutions for part 1 and 2 of the puzzle.
if __name__ == "__main__":
    bag_graph = read_input()
    # Part 1
    print(gold_possibilities(bag_graph, 'shiny gold'))
    # Part 2
    print(count_content(bag_graph, 'shiny gold') - 1)
