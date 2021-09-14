from collections import deque
from collections import Counter
from itertools import product
from random import choice
from random import sample
from itertools import permutations

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
        return str(self.value) + ', ' + str(self.suit)


def generate_hand():
    values = [*range(2, 11), "J", "Q", "K", "A"]
    suits = ["H", "D", "C", "S"]
    tpl_list = sample(list(set(product(values, suits))), 7)
    return [Card(tpl[0], tpl[1]) for tpl in tpl_list]


def get_suits(cards):
    return [card.suit for card in cards]


def get_weights(cards):
    return [card.weight for card in cards]


def get_all_straights(cards):
    unique_weights = sorted(set(get_weights(cards)))
    if len(unique_weights) < 5:
        return None
    all_straights_q = deque()
    # частный случай для самого младшего стрита с туза до 5 /
    # particular case for lowest straight from Ace to 5
    if 14 in unique_weights and 2 in unique_weights and check_consequence(unique_weights[0:4]):
        card_consequence = [cards[-1]]  # туз добавляем первым
        for unique_weight in unique_weights[0:4]:
            for card in cards:
                if unique_weight == card.weight and card.weight not in get_weights(card_consequence):
                    card_consequence.append(card)
        all_straights_q.append(card_consequence)

    # поиск всех возможных стритов по последовательности уникальных весов
    #  searching for all possible straights in hand
    for i in range(len(unique_weights)-4):
        unique_weights_slice = unique_weights[i:i + 5]
        if check_consequence(unique_weights_slice):
            card_consequence = []
            for card in cards:
                for unique_weight in unique_weights_slice:
                    if unique_weight == card.weight and card.weight not in get_weights(card_consequence):
                        card_consequence.append(card)
            all_straights_q.append(card_consequence)
    return all_straights_q


def get_max_straight(q_straight):
    if q_straight:
        return q_straight.pop()


def get_single_suit_consequence(cards):
    most_common_suit = Counter(get_suits(cards)).most_common(1)[0][0]
    return [card for card in cards if card.suit == most_common_suit]


def get_max_flush(single_suit_consequence):
    if len(single_suit_consequence) >= 5:
        return single_suit_consequence[len(single_suit_consequence) - 5:len(single_suit_consequence)]


def get_straight_flush(single_suit_consequence):
    all_straights_q = get_all_straights(single_suit_consequence)
    if all_straights_q:
        return get_max_straight(all_straights_q)


def get_royal_flush(straight_flush):
    if straight_flush[-1].weight == 14:
        return straight_flush


def get_most_frequent_cards(cards, most_common_weight):
    return [card for card in cards if card.weight == most_common_weight]


# checks if numbers of list are consequent / проверяем, идут ли числа в списке строго по порядку
def check_consequence(lst):
    return lst == list(range(min(lst), max(lst) + 1))


def sort_cards(cards):
    cards.sort(key=lambda card: card.weight)
    print("Sorted hand is:")
    for card in hand:
        print(f"{card}, weight is: {card.weight}")


def detect_combo(cards,
                 first_most_common_weight, first_most_common_weight_frequency,
                 second_most_common_weight, second_most_common_weight_frequency):
    combinations_q = deque()
    combinations_q.append(("High card", [cards[-1]]))

    straight = get_max_straight(get_all_straights(cards))
    flush = get_max_flush(get_single_suit_consequence(cards))
    straight_flush = get_straight_flush(get_single_suit_consequence(cards))

    if first_most_common_weight_frequency == 2:
        one_pair = get_most_frequent_cards(cards, first_most_common_weight)
        combinations_q.append(("one pair", one_pair))
        if second_most_common_weight_frequency == 2:
            second_pair = get_most_frequent_cards(cards, second_most_common_weight)
            two_pairs = one_pair + second_pair
            combinations_q.append(("two pair", two_pairs))

    if first_most_common_weight_frequency == 3:
        three_of_a_kind = get_most_frequent_cards(cards, first_most_common_weight)
        combinations_q.append(("three of a kind", three_of_a_kind))
        if second_most_common_weight_frequency >= 2:
            # might be lower three of a kind, so slice is taken /
            # в руке могут быть две тройки, поэтому от второй пары берем слайс
            second_pair = get_most_frequent_cards(cards, second_most_common_weight)[0:2]
            full_house = three_of_a_kind + second_pair
            combinations_q.append(("full house", full_house))

    if straight:
        combinations_q.append(("straight", straight))

    if flush:
        combinations_q.append(("flush", flush))

    if first_most_common_weight_frequency == 4:
        four_of_a_kind = get_most_frequent_cards(cards, first_most_common_weight)
        combinations_q.append(("four of a kind", four_of_a_kind))

    if straight_flush:
        combinations_q.append(("straight flush", straight_flush))
        royal_flush = get_royal_flush(straight_flush)
        if royal_flush:
            combinations_q.append(("royal flush", royal_flush))

    return combinations_q.pop()


def print_result(best_hand_tuple):
    print(f"Best combination is {best_hand_tuple[0]}:")
    for card in best_hand_tuple[1]:
        print(card)


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
hand = [Card(5, "H"), Card(2, "H"), Card(3, "C"), Card(2, "D"), Card(2, "C"), Card(3, "D"), Card(4, "S")]

# full_house + 3
# hand = [Card(3, "H"), Card(2, "H"), Card(3, "C"), Card(2, "D"), Card(2, "C"), Card(3, "D"), Card(4, "S")]

# full_house + 2 2
# hand = [Card(3, "H"), Card(2, "H"), Card(3, "C"), Card(2, "D"), Card(4, "C"), Card(3, "D"), Card(4, "S")]

# straight_flush
# hand = [Card(5, "H"), Card(2, "H"), Card(3, "H"), Card(10, "D"), Card("J", "H"), Card(4, "H"), Card("A", "H")]

# four_of_a_kind + 3
# hand = [Card(5, "H"), Card(5, "C"), Card(5, "S"), Card(5, "D"), Card(4, "C"), Card(4, "H"), Card(4, "D")]

# royal_flush
# hand = [Card("A", "H"), Card(8, "H"), Card(9, "H"), Card(10, "H"), Card("J", "H"), Card("Q", "H"), Card("K", "H")]

# WrongCombo fixed
# hand = [Card("J", "C"), Card("A", "H"), Card(9, "C"), Card(7, "H"), Card(8, "H"), Card("Q", "H"), Card("K", "H")]
# hand = generate_hand()
print("Hand is:")
for Card in hand:
    print(Card)
# sort_cards(hand)
#
# # reversed, because we need the greatest and most common
# reversed_weights = reversed(get_weights(hand))
# counters = Counter(reversed_weights).most_common(2)
# best_hand = detect_combo(hand, *counters[0], *counters[1])
# print_result(best_hand)


def count_iterable(i):
    return sum(1 for e in i)

p = permutations(hand)

print(count_iterable)
for Card in list(p):
    print(Card)
