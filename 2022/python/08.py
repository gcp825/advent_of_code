def build_grid(filepath):

    trees = dict([((y,x),height) for y,row in enumerate(open(filepath,'r').read().split('\n')) for x,height in enumerate(row)])
    max_x = max([v[::-1] for v in trees.keys()])[0]
    max_y = max(trees.keys())[0]

    return trees, max_x, max_y


def main(filepath):

    trees, xx, yy = build_grid(filepath)

    visible_from_outside, best_score = (2*xx + 2*yy, 0)

    for y, x, this_height in [(*coords,height) for coords,height in trees.items() if (0 < coords[0] < yy) and (0 < coords[1] < xx)]:

        visibility, distances = 0, []

        coords = {'n':[(n,x) for n in range(y)][::-1],  'e': [(y,n) for n in range(x+1,xx+1)],
                  's':[(n,x) for n in range(y+1,yy+1)], 'w': [(y,n) for n in range(x)][::-1]}

        for heights in [[trees[(y,x)] for y,x in coord_list] for coord_list in [coords['n'], coords['e'], coords['s'], coords['w']]]:

            tree_ct = len(heights)

            visibility = 1 if visibility == 0 and sum([1 for h in heights if h < this_height]) == tree_ct else visibility

            distances += [i+1 for i,h in enumerate(heights) if h >= this_height][:1] or [tree_ct]

        visible_from_outside += visibility
        best_score = max(best_score, distances[0] * distances[1] * distances[2] * distances[3])

    return visible_from_outside, best_score

print(main('08.txt'))