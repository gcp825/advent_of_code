def main(filepath):
   
    pairs = [tuple(map(int,y)) for y in [x.split(',') for x in open(filepath).read().replace('-',',').split('\n')]]

    return tuple(map(sum,zip(*[(1 if (a <= x <= y <= b) or (x <= a <= b <= y) else 0, 1) for a,b,x,y in pairs if min(b,y) >= max(a,x)])))

print(main('04.txt'))