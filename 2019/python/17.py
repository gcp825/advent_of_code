from intcode import IntcodeComputer    # see intcode.py in this repo
from copy import deepcopy

def determine_moves(g):

    g2   = ['.'*len(g[0])] + g + ['.'*len(g[0])];  grid = [list('.'+''.join(g2[x])+'.') for x in range(len(g2))]

    left = {'^':'<','>':'^','v':'>','<':'v'};  right = dict([(v,k) for k,v in left.items()])

    moves = [];  distance = 0;  y,x = [(y,x) for y,row in enumerate(grid) for x,z in enumerate(row) if z in '^v<>'][0];  d = grid[y][x]

    while grid[y][x] != '.':
        next_y, next_x, left_y, left_x = (y-1,x,y,x-1) if d == '^' else (y+1,x,y,x+1) if d == 'v' else (y,x-1,y+1,x) if d == '<' else (y,x+1,y-1,x)
        if grid[next_y][next_x] == '.':
            if distance > 0: 
                moves += [str(distance)]
                distance = 0
            move, d = ('L',left[d]) if grid[left_y][left_x] == '#' else ('R',right[d])
            moves += [move]
        distance += 1
        y,x = (y if d in '<>' else y-1 if d == '^' else y+1,  x if d in '^v' else x-1 if d == '<' else x+1)
        
    return moves[:-1]


def determine_input(moves):

    found = False;  m = [];  n = 0;  inp = [];  v = ['n']

    for a_len in range(1,11)[::-1]:
        possible_a = subset_generator(deepcopy(moves), a_len)
        for a, remainder_a in possible_a:        
            for i in range(len(remainder_a)):
                if remainder_a[i:i+len(a)] == a:
                    remainder_a = remainder_a[:i] + ['x'] + remainder_a[i+len(a):]

            for b_len in range(1,11)[::-1]:
                possible_b = subset_generator(deepcopy(remainder_a), b_len)
                for b, remainder_b in possible_b:
                    for j in range(len(remainder_b)):
                        if remainder_b[j:j+len(b)] == b:
                            remainder_b = remainder_b[:j] + ['x'] + remainder_b[j+len(b):]

                    possible_c = subset_generator(deepcopy(remainder_b),10)
                    c, remainder_c = next(possible_c)
                    
                    for k in range(len(remainder_c)):
                        if remainder_c[k:k+len(c)] == c:
                            remainder_c = remainder_c[:k] + ['x'] + remainder_c[k+len(c):]

                    if len(''.join(remainder_c).replace('x','')) == 0: found = True

                    if found: break
                if found: break
            if found: break
        if found: break

    while n < len(moves):
        move, n = ('A',n+len(a)) if moves[n:n+len(a)] == a else ('B',n+len(b)) if moves[n:n+len(b)] == b else ('C',n+len(c))
        m += [move]

    for cmd in (m,a,b,c,v):
        for step in cmd: 
            inp += [ord(val) for val in list(step)] + [ord(',')]
        inp.pop(-1)
        inp += [ord('\n')]

    return inp


def subset_generator(moves,length):

    while moves[0] == 'x': moves = moves[1:]
    sub = moves[:moves.index('x') if moves[:length].count('x') > 0 else length] + ['dummy']
    while len(sub) > 1:
        sub.pop(-1)
        yield sub, moves[len(sub):]


def main(f):

    grid = [x for x in [list(x) for x in ''.join([chr(x) for x in IntcodeComputer(load=f,mode='return').run()]).split('\n')] if len(x) > 0]     
    i = [(y+1,x+1) for y,r in enumerate(grid[1:-1]) for x,_ in enumerate(r[1:-1]) if ''.join(grid[y+1][x:x+3]) == '###' and grid[y][x+1] == '#' and grid[y+2][x+1] == '#']

    inp  = determine_input(determine_moves(grid))

    dust = 0
    droid = IntcodeComputer(load=f,input=inp);  droid.set_addr(0,2)
    while droid.active:
        out = droid.run()
        dust = out if droid.active else dust

    return sum([y*x for y,x in i]), dust
 
print(main('17.txt'))
