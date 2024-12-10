def get_moves(y, x, trail, my, mx):

    moves = [(yy,xx) for yy,xx in [(y-1,x),(y,x+1),(y+1,x),(y,x-1)] if 0 <= yy <= my and 0 <= xx <= mx]

    return [c for c in moves if trail[c] - trail[(y,x)] == 1]


def bfs(map):

    bounds = max(map.keys())
    score_1, score_2 = (0,0)

    for trailhead in [k for k,v in map.items() if v == 0]:

        queue, peaks = [trailhead], []

        while queue:
            moves = get_moves(*queue.pop(0), map, *bounds)
            queue += [move for move in moves if map[move] < 9]
            peaks += [move for move in moves if map[move] == 9]

        score_1 += len(set(peaks))
        score_2 += len(peaks)

    return score_1, score_2


def main(filepath):

    map = dict([((y,x),int(c)) for y,r in enumerate(open(filepath).read().split('\n')) for x,c in enumerate(r)])

    return bfs(map)


print(main('10.txt'))