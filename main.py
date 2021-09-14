from collections import Counter
from itertools import product
from random import sample
from itertools import combinations


class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        if self.value == "J":
            self.weight = 11
        elif self.value == "Q":
            self.weight = 12
        elif self.value == "K":
            self.weight = 13
        elif self.value == "A":
            self.weight = 14
        else:
            self.weight = value

    def __str__(self):
        return str(self.value) + str(self.suit)


def generate_hand():
    values = [*range(2, 11), "J", "Q", "K", "A"]
    suits = ["H", "D", "C", "S"]
    tpl_list = sample(list(set(product(values, suits))), 7)
    return [Card(tpl[0], tpl[1]) for tpl in tpl_list]


def get_suits(cards):
    return [card.suit for card in cards]


def get_weights(cards):
    return [card.weight for card in cards]


def check_straight(cards):
    weights = get_weights(cards)
    if 14 in weights and 2 in weights and check_consequence(sorted(weights)[0:4]):
        return True
    return check_consequence(weights)


def check_equal_suite(cards):
    return len(set(get_suits(cards))) == 1


def check_royal_flush(straight_flush):
    # return straight_flush[-1].weight == 14
    return [*range(10, 15)] == sorted(get_weights(straight_flush))


# checks if numbers of list are consequent / проверяем, идут ли числа в списке строго по порядку
def check_consequence(lst):
    return lst == list(range(min(lst), max(lst) + 1))


def sort_cards(cards):
    return cards.sort(key=lambda card: card.weight)


def detect_combo(hand):
    sort_cards(hand)
    if check_equal_suite(hand):
        if check_straight(hand):
            if check_royal_flush(hand):
                return 9, "Royal Flush"
            return 8, "Straight Flush"
        return 5, "Flush"
    elif check_straight(hand):
        return 4, "Straight"

    else:
        counters = Counter(reversed(get_weights(hand))).most_common(2)
        if counters[0][1] == 4:
            return 7, "Four of kind"
        if counters[0][1] == 3:
            if counters[1][1] == 2:
                return 6, "Full house"
            return 3, "Three of kind"
        if counters[0][1] == 2:
            if counters[1][1] == 2:
                return 2, "Two pairs"
            return 1, "One pair"
    return 0, "High card"


def get_max_hand(hand):
    combos = list(combinations(hand, 5))
    res = {}
    for cards in combos:
        combo = detect_combo(list(cards))
        res[combo[0]] = combo[1]
    print("Max combo is: " + res[max(res.keys())])


# one pair
# hand = [Card(9, "H"), Card(8, "H"), Card("A", "C"), Card(4, "D"), Card(2, "C"), Card(3, "H"), Card(9, "S")]

# two pair
# hand = [Card(7, "H"), Card(8, "H"), Card(3, "C"), Card(2, "D"), Card(2, "C"), Card(3, "H"), Card(9, "S")]

# 3 two pair
# hand = [Card(9, "H"), Card(9, "H"), Card(3, "C"), Card(2, "D"), Card(2, "C"), Card(3, "H"), Card(10, "S")]

# three
# hand = [Card(3, "S"), Card(5, "H"), Card(3, "C"), Card(2, "D"), Card(4, "C"), Card(3, "H"), Card(9, "H")]

# straight
# hand = [Card("J", "C"), Card("A", "H"), Card(9, "C"), Card(7, "H"), Card(8, "H"), Card(10, "C"), Card("K", "H")]

# straight + two pair
# hand = [Card(2, "C"), Card(2, "H"), Card(3, "C"), Card(3, "S"), Card(4, "H"), Card(5, "H"), Card(6, "H")]
# hand = [Card(2, "H"), Card(3, "C"), Card(3, "S"), Card(4, "H"), Card(4, "C"), Card(5, "H"), Card("A", "H")]

# several_straights
# hand = [Card(2, "H"), Card(3, "H"), Card(4, "C"), Card(5, "S"), Card(6, "H"), Card(7, "H"), Card(8, "C")]

# straight + 3
# hand = [Card("A", "H"), Card(2, "H"), Card(3, "D"), Card(3, "D"), Card(3, "C"), Card(4, "S"), Card(5, "D")]

# flush
# hand = [Card("A", "H"), Card(2, "H"), Card(3, "H"), Card(10, "H"), Card("J", "C"), Card("K", "H"), Card("Q", "H")]

# full_house
# hand = [Card(5, "H"), Card(2, "H"), Card(3, "C"), Card(2, "D"), Card(2, "C"), Card(3, "D"), Card(4, "S")]

# full_house + 3
# hand = [Card(3, "H"), Card(2, "H"), Card(3, "C"), Card(2, "D"), Card(2, "C"), Card(3, "D"), Card(4, "S")]

# full_house + 2 2
# hand = [Card(3, "H"), Card(2, "H"), Card(3, "C"), Card(2, "D"), Card(4, "C"), Card(3, "D"), Card(4, "S")]

# straight_flush
# hand = [Card(5, "H"), Card(2, "H"), Card(3, "H"), Card(6, "C"), Card(7, "H"), Card(4, "H"), Card("A", "H")]

# four_of_a_kind + 3
# hand = [Card(5, "H"), Card(5, "C"), Card(5, "S"), Card(5, "D"), Card(4, "C"), Card(4, "H"), Card(4, "D")]

# royal_flush
# hand = [Card("A", "H"), Card(8, "H"), Card(9, "H"), Card(10, "H"), Card("J", "H"), Card("Q", "H"), Card("K", "H")]

# WrongCombo fixed
# hand = [Card("J", "C"), Card("A", "H"), Card(9, "C"), Card(7, "H"), Card(8, "H"), Card("Q", "H"), Card("K", "H")]

hand = generate_hand()
print("Hand is:")
print(*hand)
# sort_cards(hand)

# # reversed, because we need the greatest and most common
# reversed_weights = reversed(get_weights(hand))
# counters = Counter(reversed_weights).most_common(2)
# best_hand = detect_combo(hand, *counters[0], *counters[1])
# print_result(best_hand)
get_max_hand(hand)



