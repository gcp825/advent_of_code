
def exchange(x,a,b): return x[:a] + x[b] + x[a+1:b] + x[a] + x[b+1:]
def partner(x,a,b):  return exchange(x,*sorted((x.find(a),x.find(b))))
def spin(x,n):       return x[n*-1:] + x[:n*-1]

def move_cycle(formation,moves,cycles=0):

    for move, programs in moves:
        formation = spin(formation,*programs) if move == 's' else partner(formation,*programs) if move == 'p' else exchange(formation,*programs)

    return formation, cycles+1

def main(filepath):

    start_formation = 'abcdefghijklmnop'
    moves = [(x,y) if x == 'p' else (x,tuple(sorted(map(int,y)))) for x,y in [(x[0],tuple(x[1:].split('/'))) for x in open(filepath,'r').read().split(',')]]
    total_cycles = 1000**3

    formation, cycles = move_cycle(start_formation,moves)
    first_formation = formation

    while cycles < total_cycles:
        formation, cycles = move_cycle(formation,moves,cycles)
        if formation == start_formation:
            cycles = total_cycles - (total_cycles%cycles)

    return first_formation, formation

print(main('16.txt'))
