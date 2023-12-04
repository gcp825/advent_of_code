def parse_input(filepath):

    input = [x[x.find(':')+1:].strip().split(' | ') for x in open(filepath).read().split('\n')]
    cards = [(parse_numbers(x), parse_numbers(y)) for x,y in input]

    return cards, dict([(i,1) for i in range(len(cards))])


def parse_numbers(raw_numbers):

    return [int(n) for n in raw_numbers.strip().replace('  ',' ').split(' ')]


def main(filepath):

    scratchcards, card_counts = parse_input(filepath)

    matches = [len([n for n in numbers if n in winning_numbers]) for winning_numbers, numbers in scratchcards]

    for this_card_id, matched_number_count in zip(card_counts.keys(), matches):
        for card_id in range(this_card_id + 1, this_card_id + 1 + matched_number_count):
            card_counts[card_id] += card_counts[this_card_id] 

    return sum([2**(n-1) for n in matches if n > 0]), sum(card_counts.values())

print(main('04.txt'))