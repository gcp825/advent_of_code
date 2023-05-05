def main(filepath):

    route = open(filepath).read().rstrip('\n')[1:-1]
    y,x,distance = (0,0,0)
    distances,stack = (dict(),[])

    parse = {'N': lambda: (y-1,x,distance+1),
             'E': lambda: (y,x+1,distance+1),
             'S': lambda: (y+1,x,distance+1),
             'W': lambda: (y,x-1,distance+1),
             '(': lambda: stack.append((y,x,distance)) or (y,x,distance),
             '|': lambda: stack[-1],
             ')': lambda: stack.pop(-1)}

    for char in route:
        y,x,distance = parse[char]()
        distances[(y,x)] = min(distance,distances.get((y,x),distance))

    return max([v for v in distances.values()]), len([v for v in distances.values() if v >= 1000])


print(main('20.txt'))