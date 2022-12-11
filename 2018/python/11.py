#  Absolutely horrific, ugly and glacially slow brute force solution.
#  I'm sure there's something much more intelligent I could be doing to reuse previously calculated scores here, but even then I can't see
#  how that would yield a properly fast solution. I'm definitely missing a trick somewhere with this one.
#  This could also be refactored to use a list comprehension instead of the inner for loop, but that seems pointless when the whole thing needs a rewrite!

def main(serial=9435):

    cells         = dict([((x,y),int(('00'+str((((x+10)*y)+serial)*(x+10)))[-3])-5) for x in range(1,301) for y in range(1,301)])
    latest_scores = [(v,k) for k,v in sorted(cells.items())]
    scores        = {1:latest_scores}

    for z in range(2,301):

        within_grid   = [(c,p) for p,c in latest_scores if c[0]+z-1 <= 300 and c[1]+z-1 <= 300]
        latest_scores = []

        for coords, power in within_grid: 

            p,x,y = power, coords[0]+z-1, coords[1]

            while y <= coords[1]+z-1:  
                p += cells[(x,y)]
                y += 1

            x = coords[0]
            y -= 1

            while x < coords[0]+z-1:
                p += cells[(x,y)]
                x += 1

            latest_scores += [(p,coords)]

        scores[z] = latest_scores

    return max(scores[3])[1], [(*square[1],size) for square,size in sorted([(max(v),k) for k,v in scores.items()])][-1]

print(main())