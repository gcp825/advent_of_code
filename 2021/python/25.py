# Nice straightforward one to finish. Wrapping around the grid dealt with by mod. Seems to be much quicker to recreate the seabed as a list than a dict.

def main(filepath):

    seabed, old_seabed = [list(x) for x in open(filepath,'r').read().split('\n')], []

    moves = 0;  e,s,f = ('>','v','.');  xx, yy = len(seabed[0]), len(seabed)

    while seabed != old_seabed:

        moves += 1
        old_seabed = [] + seabed

        seabed = [] + [[e if (val == f and seabed[y][(x-1)%xx] == e)                                     else                     
                        s if (val == f and seabed[(y-1)%yy][x] == s)                                     else
                        s if (val == e and seabed[(y-1)%yy][x] == s and seabed[y][(x+1)%xx] == f)        else
                        f if (val == e and seabed[y][(x+1)%xx] == f)                                     else
                        f if (val == s and seabed[(y+1)%yy][x] == e and seabed[(y+1)%yy][(x+1)%xx] == f) else
                        f if (val == s and seabed[(y+1)%yy][x] == f and seabed[(y+1)%yy][(x-1)%xx] != e) else val for x,val in enumerate(row)] 
                                                                                                                  for y,row in enumerate(seabed)] 

    return moves
     
print(main('25.txt'))