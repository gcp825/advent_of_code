from collections import Counter

def parse_input(filepath,jokers=False):

    swap = lambda x: x.replace('J','*') if jokers else x

    return [(h,int(b)) for h,b in [x.split(' ') for x in swap(open(filepath).read()).split('\n')]]


def calculate_winnings(hands):

    ranking = lambda x: (type_rank(x), card_order_rank(x))

    return sum([(i+1)*b for i,(_,b) in enumerate(sorted([(ranking(cards),bid) for cards, bid in hands]))])


def type_rank(cards):

    counts = Counter(cards)
    regular_cards = [x[::-1] for x in sorted([(n,c) for c,n in counts.items() if c != '*'])[::-1]]
    jokers_applied = [(c,n + counts.get('*',0)) for c,n in regular_cards[:1]] + regular_cards[1:] if regular_cards else [('*',5)]

    return ''.join([str(n) for _,n in jokers_applied])


def card_order_rank(cards):

    ranks = dict([x[::-1] for x in enumerate('*23456789TJQKA')])

    return tuple([ranks[card] for card in cards])


def main(filepath):

    jacks = parse_input(filepath)
    jokers = parse_input(filepath,True)

    return calculate_winnings(jacks), calculate_winnings(jokers)


print(main('07.txt'))