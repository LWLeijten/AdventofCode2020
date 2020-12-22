from copy import copy


def read_player_cards(filename):
    """ Reads a deckfile for a player and returns it as a list of cards."""
    deck = []
    with open(f'solutions/day22/{filename}') as f:
        for line in f:
            deck.append(int(line.strip()))
    return deck


def play_combat(p1, p2):
    """ Plays a game of regular combat.
        Returns the final decks of player 1 and player 2."""
    while len(p1) > 0 and len(p2) > 0:
        p1_card, p2_card = p1.pop(0), p2.pop(0)
        if p1_card > p2_card:
            p1 += [p1_card, p2_card]
        else:
            p2 += [p2_card, p1_card]
    return p1, p2


def play_recursive_combat(p1, p2):
    """ Plays a game of recursive combat. Keeping track of what states have been
        seen before to prevent infinite loops. Returns the resulting decks of a 
        recursive combat game and a boolean indicating if player1 won or not.
        This boolean is needed to determine what action to take after a nested game. """
    seen_states = []
    while p1 and p2 and not [p1, p2] in seen_states:
        seen_states.append([copy(p1), copy(p2)])
        p1_card, p2_card = p1.pop(0), p2.pop(0)
        if p1_card <= len(p1) and p2_card <= len(p2):
            _, _, p1win = play_recursive_combat(
                copy(p1)[:p1_card], copy(p2)[:p2_card])
            if p1win:
                p1 += [p1_card, p2_card]
            else:
                p2 += [p2_card, p1_card]
        else:
            if p1_card > p2_card:
                p1 += [p1_card, p2_card]
            else:
                p2 += [p2_card, p1_card]
    return p1, p2, len(p1) > 0


def calculate_score(p):
    """ Calculates a players score by its deck contents. """
    return sum([(i+1) * card for i, card in enumerate(reversed(p))])


# Find the solutions for part 1 and 2 of the puzzle.
if __name__ == "__main__":
    p1 = read_player_cards('player1.txt')
    p2 = read_player_cards('player2.txt')
    # Part 1
    resultp1, resultp2 = play_combat(copy(p1), copy(p2))
    print(
        f"Final score of Combat: p1 {calculate_score(resultp1)} VS p2 {calculate_score(resultp2)}")
    # Part 2
    resultp1, resultp2, _ = play_recursive_combat(copy(p1), copy(p2))
    print(
        f"Final score of Recursive Combat: p1 {calculate_score(resultp1)} VS p2 {calculate_score(resultp2)}")
