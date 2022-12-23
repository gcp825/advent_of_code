def get_move(y,x,grid,move_order): 

    moves = dict()

    if (y-1,x-1) not in grid and (y-1,x) not in grid and (y-1,x+1) not in grid:  moves['N'] = (y-1,x)
    if (y+1,x-1) not in grid and (y+1,x) not in grid and (y+1,x+1) not in grid:  moves['S'] = (y+1,x)
    if (y-1,x+1) not in grid and (y,x+1) not in grid and (y+1,x+1) not in grid:  moves['E'] = (y,x+1)
    if (y-1,x-1) not in grid and (y,x-1) not in grid and (y+1,x-1) not in grid:  moves['W'] = (y,x-1)

    if len(moves) in (0,4): return (y,x)
    else:
        for direction in move_order:
            if direction in moves:
                return moves[direction]


def score(grid):

    min_y = min(grid)[0]
    max_y = max(grid)[0]
    min_x = min([x[::-1] for x in grid])[0]
    max_x = max([x[::-1] for x in grid])[0]

    return ((max_y-min_y+1) * (max_x-min_x+1)) - len(grid)
    

def main(filepath):

    grid = set([(y,x) for y,row in enumerate(open(filepath).read().split('\n')) for x,val in enumerate(row) if val == '#'])

    move_order = 'NSWE'

    round = 0;  part1 = None;  updated = True

    while updated:

        round += 1;  current = list(grid);  moves = [];  clashes = set();  updated = False

        for y,x in grid:

            move = get_move(y,x,grid,move_order)
            if move in moves:
                clashes.add(move)
            moves.append(move)

        for elf, move in list(zip(current,moves)):

            if elf != move and move not in clashes:
                grid.remove(elf)
                grid.add(move)
                if not updated: 
                    updated = True

        move_order = move_order[1:] + move_order[0] 

        if round == 10: part1 = score(grid)


    return part1, round


print(main('23.txt'))