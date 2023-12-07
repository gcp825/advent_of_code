# I'm sure this could be much slicker, but limited time for this today, so for now: it is what it is...

from collections import Counter

def parse_input(filepath):

    return [(h,int(b)) for h,b in [x.split(' ') for x in open(filepath).read().split('\n')]]


def calculate_winnings(hands,jokers=False):

    return sum([(i+1)*b for i,(_,b) in enumerate(sorted([(ranking(cards,jokers),bid) for cards, bid in hands]))])


def ranking(cards,jokers):

    return (type_rank(cards,jokers), card_order_rank(cards,jokers))


def type_rank(cards,jokers):

    counts = sorted([(ct, card) for card, ct in Counter(list(cards)).items()])

    if jokers and 'J' in cards and len(counts) > 1:
        counts = apply_jokers(counts)

    distinct_cards = len(counts)

    if   distinct_cards == 5: rank = 0
    elif distinct_cards == 4: rank = 1
    elif distinct_cards == 3 and counts[2][0] == 2: rank = 2
    elif distinct_cards == 3 and counts[2][0] == 3: rank = 3
    elif distinct_cards == 2 and counts[1][0] == 3: rank = 3.2
    elif distinct_cards == 2 and counts[1][0] == 4: rank = 4
    elif distinct_cards == 1: rank = 5
    else:
        raise ValueError(f"What sort of hand is this?!: {cards}")

    return rank


def apply_jokers(counts):

    i, jokers = [(i,ct) for i,(ct,c) in enumerate(counts) if c == 'J'][0]
    no_jokers = counts[:i] + counts[i+1:]

    return no_jokers[:-1] + [(no_jokers[-1][0] + jokers, no_jokers[-1][1])]


def card_order_rank(cards,jokers):

    ranks = dict(zip(list('23456789TJQKA'),range(1,14)))
    if jokers: ranks['J'] = 0

    return tuple([ranks[card] for card in cards])


def main(filepath):

    hands = parse_input(filepath)

    return calculate_winnings(hands), calculate_winnings(hands,True)


print(main('07.txt'))