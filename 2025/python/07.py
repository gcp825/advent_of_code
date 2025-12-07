def parse_input(f):

    return {(y,x):val for y,row in enumerate(open(f).read().split('\n')) for x,val in enumerate(row)}


def count_timelines(grid):

    new_timelines = {k:1 for k,v in grid.items() if v == 'S'}
    diverged_timelines, total_timelines = (0,0)

    while new_timelines:
        current_timelines, new_timelines = new_timelines, dict()
        for (y,x), timeline_ct in current_timelines.items():
            if (y+1,x) in grid:
                if grid[(y+1,x)] == '^':
                    diverged_timelines += 1
                    for coords in [(y+1,n) for n in (x-1,x+1) if (y+1,n) in grid]:
                        new_timelines[coords] = new_timelines.get(coords,0) + timeline_ct
                else:
                    new_timelines[(y+1,x)] = new_timelines.get((y+1,x),0) + timeline_ct
            else:
                total_timelines += timeline_ct

    return diverged_timelines, total_timelines


def main(filepath):

    return count_timelines(parse_input(filepath))


print(main('07.txt'))