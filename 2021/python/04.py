#  This whole thing feels very crude, but it seemed like the easiest and quickest approach, and it copes with bingo cards of any size 
#  and any selection of (positive) integers - so it's fine. Refactored to use list comprehensions on the parsing and card marking.
#
#  Spent longer than I should have on part 2 by first trying to leave winning cards in place but invalidating the values on them when 
#  looping through (which then tripped up my scoring...) rather than just doing the obvious and removing them from the list. I'm an idiot.

from itertools import chain

def play_game(nbrs,cards):

    for n in nbrs:
        cards = mark_cards(n,cards)
        winner, card_id = check_cards(cards)
        if winner: break

    return cards, card_id, n

def mark_cards(n,cards):      #  Called numbers set negative (and zero handled by setting to -0.5)

    return [[[nbr if n != nbr else max(n,0.5)*-1 for nbr in row] for row in card] for card in cards]  

def check_cards(cards):

    winner = False

    for i, card in enumerate(cards):

        for row in card:
            winner = validate_line(row)
            if winner: break

        if not winner:
            transposed_card = list(zip(*card))
            for col in transposed_card:
                winner = validate_line(col)
                if winner: break

        if winner: break

    return winner, i

def validate_line(line): return True if max(line) < 0 else False

def score_card(card): return sum([x for x in list(chain(*card)) if x >= 0])

def main(filepath):

    nbrs   = [int(x) for x in open(filepath,'r').read().split('\n')[0].split(',')]
    cards  = [[list(map(int,y.split())) for y in x.split('\n')] for x in open(filepath,'r').read().split('\n\n')[2:]]
    scores = []

    for i in range(len(cards)):

        cards, winning_card, winning_nbr = play_game(nbrs,cards)
        scores += [score_card(cards[winning_card]) * winning_nbr]

        cards = cards[:winning_card] + cards[winning_card+1:]   #  Remove winning card
        nbrs  = nbrs[nbrs.index(winning_nbr):]                  #  Remove already called numbers

    return scores[0],scores[-1]

print(main('04.txt'))