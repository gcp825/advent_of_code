#  Things to note about this code...
#
#  1) I don't like dealing with negative coordinates if I don't have to, so I've rotated the chamber 90 degrees clockwise so that 
#     rocks start at the right of the chamber and fall to the left. Hence the height calculation using the x coordinate.
#
#  2) It's slow, I think because for convenience / reuse of previous code all of my rock unit coordinates are stored in tuples. 
#     Endlessly having to tuple(map(sum,zip( those seems to be taking a toll... so it really needs a performance refactor.


def setup_rocks():

    a = [(3,4),(4,4),(5,4),(6,4)]
    b = [(4,4),(3,5),(4,5),(5,5),(4,6)]
    c = [(3,4),(4,4),(5,4),(5,5),(5,6)]
    d = [(3,4),(3,5),(3,6),(3,7)]
    e = [(3,4),(4,4),(3,5),(4,5)]

    return [a,b,c,d,e]


def apply_jet(rock, grid, jet_pattern, jet_cycle):

    jet = jet_pattern[jet_cycle % len(jet_pattern)]

    if (min(rock)[0] > 1 and jet == '<') or (max(rock)[0] < 7 and jet == '>'): 

        moved_rock = [tuple(map(sum,zip(coords,({'<':-1,'>':1}[jet],0)))) for coords in rock]

        if not [c for c in moved_rock if c in grid]:

            rock = moved_rock

    return rock, jet_cycle+1


def tower_height(grid,adjust=0): return max([x[::-1] for x in grid])[0] + adjust


def main(filepath,number_of_rocks):

    jet_pattern = open(filepath).read()
    rocks       = setup_rocks()
    grid        = set()
    snapshot    = []
    rock_ct     = 0
    jet_cycle   = 0
    height_adjustment = 0


    while rock_ct < number_of_rocks:

        #  Place and drop the next rock

        offset = 0 if len(grid) == 0 else max([x[::-1] for x in grid])[0]

        rock_ct += 1
        rock     = [tuple(map(sum,zip(coords,(0,offset)))) for coords in rocks[(rock_ct-1)%5]]

        rock, jet_cycle = apply_jet(rock,grid,jet_pattern,jet_cycle)

        while not [c for c in [tuple(map(sum,zip(coords,(0,-1)))) for coords in rock] if c in grid or c[1] <= 0]:

            rock = [tuple(map(sum,zip(coords,(0,-1)))) for coords in rock]

            rock, jet_cycle = apply_jet(rock,grid,jet_pattern,jet_cycle)

        grid.update(rock)


        #  If the top of the rock tower is now a flat surface the width of the chamber i.e  #######
        #  then snapshot the rock count, the type of rock just dropped and the height of the rock tower.

        #  When we see this combination again, use the current rock count and tower height versus the snapshot to determine
        #  the rock count & height diffs between occurences and use this to fast forward the rock count and tower height.

        #  We should probably check for a congruence of the jet pattern as well here, but we don't need to with this jet pattern input...
        #  presumably it has been created to be always congruent with this combination, and that this is true for all actual inputs.


        if sum([1 if (y,x) in grid else 0 for y in range(1,8) for x in [tower_height(grid)]]) == 7:

            if snapshot:

                if snapshot[1] == rocks[(rock_ct-1)%5]:

                    cycle_period = rock_ct - snapshot[0]
                    cycle_height = tower_height(grid) - snapshot[2]

                    remaining_rocks = number_of_rocks - rock_ct

                    height_adjustment = (remaining_rocks//cycle_period) * cycle_height

                    rock_ct = number_of_rocks - (remaining_rocks % cycle_period)

            else:

                snapshot += [rock_ct, rocks[(rock_ct-1)%5], tower_height(grid)]


    return tower_height(grid,height_adjustment)

print((main('17.txt',2022), main('17.txt',1000000000000)))
