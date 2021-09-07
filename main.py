from random import sample
from collections import deque
from collections import Counter


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
        # return str(self.value) + ', ' + str(self.suit) + ', ' + "weight is: " + str(self.weight)
        return str(self.value) + ', ' + str(self.suit)


# а нафига генерировать всю колоду, если тебе нужно только 7 карт?
def generate_cards():
    values = [*range(2, 11), "J", "Q", "K", "A"]
    suits = ["H", "D", "C", "S"]
    return [Card(i, j) for i in values for j in suits]


def generate_hand(cards):
    return sample(cards, 7)


def get_suits(cards):
    return [Card.suit for Card in cards]


def get_weights(cards):
    return [Card.weight for Card in cards]


def get_all_straights(cards):
    unique_weights = set(get_weights(cards))
    q = deque()
    if len(unique_weights) >= 5:
        if 14 in unique_weights:
            if 2 in unique_weights:
                card_consequence = cards[0:4]
                weight_consequence = get_weights(card_consequence)
                if check_consequence(weight_consequence):
                    weight_consequence.append(14)
                    card_consequence.insert(0, cards[-1])
                    q.append(card_consequence)

        weights = get_weights(cards)
        for i in range(3):
            card_consequence = cards[i:i + 5]
            weight_consequence = weights[i:i + 5]
            if check_consequence(weight_consequence):
                q.append(card_consequence)

    return q


def get_max_straight(q_straight):
    if q_straight:
        return q_straight.pop()
    return []


def get_single_suit_consequence(cards):
    single_suit_consequence = []
    most_common_suit = Counter(get_suits(cards)).most_common(1)[0][0]
    for Card in cards:
        if Card.suit == most_common_suit:
            single_suit_consequence.append(Card)
    return single_suit_consequence


def get_max_flush(single_suit_consequence):
    if len(single_suit_consequence) >= 5:
        return single_suit_consequence[len(single_suit_consequence) - 5:len(single_suit_consequence)]
    return []


def get_straight_flush(single_suit_consequence):
    q = get_all_straights(single_suit_consequence)
    if q:
        return get_max_straight(q)
    return []


def get_royal_flush(straight_flush):
    if straight_flush[-1].weight == 14:
        return straight_flush
    return []


def check_consequence(lst):
    return lst == list(range(min(lst), max(lst) + 1))


def detect_combo(cards):
    cards.sort(key=lambda Card: Card.weight)
    print("Sorted hand is:")
    for Card in hand:
        print(f"{Card}, weight is: {Card.weight}")

    # searching all combinations
    combinations_q = deque()

    combinations_q.append(("High card", [cards[-1]]))
    straight = get_max_straight(get_all_straights(cards))
    flush = get_max_flush(get_single_suit_consequence(cards))
    straight_flush = get_straight_flush(get_single_suit_consequence(cards))

    # lower combinations
    if straight:
        combinations_q.append(("straight", straight))
    if flush:
        combinations_q.append(("flush", flush))
    # full_house
    # four of a kind
    if straight_flush:
        combinations_q.append(("straight flush", straight_flush))
        royal_flush = get_royal_flush(get_straight_flush(get_single_suit_consequence(cards)))
        if royal_flush:
            combinations_q.append(("royal flush", royal_flush))

    best_hand_tuple = combinations_q.pop()
    print(f"Best combination is {best_hand_tuple[0]}:")
    for Card in best_hand_tuple[1]:
        print(Card)


# hardcode:
# straight
# hand = [Card("A", "H"), Card(2, "H"), Card(3, "D"), Card(4, "D"), Card(5, "C"), Card("J", "S"), Card("Q", "S")]
# hand = [Card("A", "H"), Card(2, "H"), Card(3, "D"), Card(4, "D"), Card(5, "C"), Card("K", "S"), Card("Q", "S")]
# hand = [Card("A", "H"), Card(2, "H"), Card(3, "D"), Card(10, "D"), Card("J", "C"), Card("K", "S"), Card("Q", "S")]
# hand = [Card("A", "H"), Card("A", "S"), Card(10, "D"), Card(9, "D"), Card("J", "C"), Card("K", "S"), Card("Q", "S")]
# flush
# hand = [Card("A", "H"), Card(2, "H"), Card(3, "H"), Card(10, "H"), Card("J", "C"), Card("K", "H"), Card("Q", "H")]
# straight_flush
# hand = [Card(5, "H"), Card(2, "H"), Card(3, "H"), Card(10, "D"), Card("J", "C"), Card(4, "H"), Card("A", "H")]
# royal_flush
# hand = [Card("A", "H"), Card(8, "H"), Card(9, "H"), Card(10, "H"), Card("J", "H"), Card("Q", "H"), Card("K", "H")]

# real code:
pack = generate_cards()
hand = generate_hand(pack)
print("Hand is:")
for Card in hand:
    print(Card)

detect_combo(hand)
