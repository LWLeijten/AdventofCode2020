from typing import List


class Cup():
    """ A cup. Has a label and a pointer to the cup next to it clockwise. """

    def __init__(self, label):
        self.label = label
        self.next = None


class CupCircle():
    """ Circular linked list representing the cup circle. Each node is a cup. """

    def display(self):
        """ Displays the cupcircle as a number string. """
        current = self.head
        output = str(current.label)
        while(current.next != self.head):
            current = current.next
            output += str(current.label)
        print(f"The circle is as follows: {output}")

    def __init__(self, max_cup):
        """ Inits an empty cup circle """
        self.max_cup = max_cup
        self.head = Cup(None)
        self.tail = Cup(None)
        self.head.next = self.tail
        self.tail.next = self.head
        self.cup_lookup = dict()

    def add_cup(self, label):
        """ Adds a cup to the cupcircle. """
        new_cup = Cup(label)
        if self.head.label == None:
            self.head = new_cup
            self.tail = new_cup
            new_cup.next = self.head
        else:
            self.tail.next = new_cup
            self.tail = new_cup
            self.tail.next = self.head
        self.cup_lookup[label] = new_cup

    def get_destination_cup(self, cur_cup, pickups):
        """ Given the current cup and the currently picked up cups,
            returns the new destination cup. """
        destination = cur_cup.label - 1
        while destination in list(map(lambda c: c.label, pickups)) or destination == 0:
            destination -= 1
            if destination < 1:
                destination = self.max_cup
        return self.cup_lookup[destination]

    def play(self, cur_cup):
        """ Given the current cup, plays a round of the game.
            Returns the new current cup. """
        pickups: List[Cup] = [cur_cup.next,
                              cur_cup.next.next,
                              cur_cup.next.next.next]
        cur_cup.next = pickups[2].next
        destination_cup = self.get_destination_cup(cur_cup, pickups)
        old_followup = destination_cup.next
        destination_cup.next = pickups[0]
        pickups[2].next = old_followup
        return cur_cup.next


if __name__ == "__main__":
    # Part 1
    input_nums = [4, 7, 6, 1, 3, 8, 2, 5, 9]
    circle = CupCircle(max_cup=max(input_nums))
    for num in input_nums:
        circle.add_cup(num)
    cur_cup = circle.head
    for i in range(100):
        cur_cup = circle.play(cur_cup)
    circle.display()

    # Part 2
    input_nums += list(range(10, 1000001))
    circle2 = CupCircle(max_cup=max(input_nums))
    for num in input_nums:
        circle2.add_cup(num)
    cur_cup = circle2.head
    for i in range(10000000):
        cur_cup = circle2.play(cur_cup)
    cup1, cup2 = circle2.cup_lookup[1].next,  circle2.cup_lookup[1].next.next
    print(cup1.label * cup2.label)
