#  Ugh. Couldn't face doing this recursively, it was difficult enough to get my head around the logic already.
#
#  Went with a dynamic programming approach that works through each row group by group, recording the number
#  number of valid spring permutations that end at each index, and carries those totals through cumulatively
#  to the next group calculation e.g.
#
#  If a row contains 2 groups, and there are 3 permutations for Group 0 ending at index 5, and 10 permutations 
#  for Group 1 beginning at index 6 and ending at index 12, there are 30 (10x3) overall permutations that
#  end at index 12.
#
#  Without recursion or any optimisations that prune the queue so that it only contains viable solutions at the 
#  earliest possible point, this takes 9.5 seconds to run on my laptop. With both those things, I would guess
#  this probably comes in at 2-3 seconds. But this was pretty nightmarish, so I'm content with it as is.

def parse_input(filepath):

    return [(x + '.', tuple(map(int,y.split(',')))) for x,y in [z.split(' ') for z in open(filepath).read().split('\n')]]


def permutations(row,pattern):

    totals = {0:1}

    for pattern_idx, target_grp_length in enumerate(pattern):

        perms = dict()
        final_group = True if pattern_idx+1 == len(pattern) else False

        for row_idx, cumulative_perms in totals.items():
            queue = [(row_idx,0)]
            while queue:
                idx, current_grp_length = queue.pop(0)
                if idx < len(row):
                    for move in ["#","."] if row[idx] == '?' else [row[idx]]:

                        if (move == '.' and current_grp_length == target_grp_length
                        and (not final_group or (final_group and '#' not in row[idx+1:]))):

                            perms[idx+1] = perms.get(idx+1,0) + cumulative_perms
                            
                        elif move == '.' and current_grp_length == 0: queue += [(idx+1,0)]
                        elif move == '#':                             queue += [(idx+1,current_grp_length+1)]
        
        totals = dict([(i,p) for i,p in perms.items() if p > 0])

    return sum(totals.values())


def sum_permutations(springs):

    return sum([permutations(row,pattern) for row,pattern in springs])


def main(filepath):

    springs = parse_input(filepath)
    unfolded_springs = [('?'.join([row[:-1]]*5) + '.', pattern*5) for row, pattern in springs]

    return sum_permutations(springs), sum_permutations(unfolded_springs)


print(main('12.txt'))