#  Well, I did say I thought I could brute force it, and I did, with no recursion or memoization. But it is comically slow!
#  The two queue approach and pop of the state dictionary helps to avoid this blowing up with an out of memory error.
#  This one is going to get a rewrite when I've got time... this is a perfect opportunity to look at lru_cache and how to best utilise that.
#  Howvever, just reading the solutions megathread once I'd finished, I was annoyed to see such an obvious alternative approach that I just 
#  didn't see (you don't need to actually play the games and alternate players... just work out when each player hits 21+ for all valid 
#  sequences of their moves alone, then combine both sets of info to work out the winners). Its too easy to get locked into just one thought 
#  of how to solve it.

from collections import deque, Counter
from itertools import product
from functools import reduce
from operator import mul as multiply

def deterministic_die(positions,rolls=3,board=10,target=1000):

    players = [(positions[0],0), (positions[1],0)]

    moves = deque(range(1,board+1)[::-1])
    moves.rotate(sum(range(rolls+1))-board)
    player, turns = (0,0)

    while True:

        position, score, moves = roll(*players[player],moves,board)
        players[player] = (position,score)
        turns += 1
        if score >= target: break
        else:
            player = abs(player-1)

    return min([p[1] for p in players]) * turns * rolls

def roll(position,current_score,moves,board):

    score = (moves[0]+position)%board
    score = board if score == 0 else score
    position = score
    current_score += score
    moves.rotate(-1)

    return position, current_score, moves

def quantum_die(positions,rolls=3):

    roll_combination_ct = Counter([sum(x) for x in list(product((1,2,3),repeat=rolls))])
    roll_combinations = list(roll_combination_ct.keys())

    player_one, player_two = (0,0)

    queue = deque([[]])
    state = dict([(tuple(),(0,*positions,0))])
    
    while len(queue) > 0:

        moves = queue.popleft()
        current_state = state.pop(tuple(moves))
        turn = len(moves)
        switch = turn%2
        inner_queue = deque([moves + [x] for x in roll_combinations])

        while len(inner_queue) > 0: 

            expanded_moves = inner_queue.popleft()

            s1,p1,p2,s2 = current_state if switch == 0 else current_state[::-1]

            p1 = (expanded_moves[-1]+p1-1)%10 + 1
            s1 += p1

            if s1 >= 21:

                universes = reduce(multiply,[roll_combination_ct[x] for x in expanded_moves])
                player_one += universes if switch == 0 else 0
                player_two += universes if switch == 1 else 0

            else:
                state[tuple(expanded_moves)] = (s1,p1,p2,s2) if switch == 0 else (s2,p2,p1,s1)
                queue.extend([expanded_moves])

    return max(player_one, player_two)

def main(positions):

    pt1 = deterministic_die(positions)
    pt2 = quantum_die(positions)

    return pt1,pt2

print(main((2,5)))