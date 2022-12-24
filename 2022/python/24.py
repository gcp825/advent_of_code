def main(f,trips=3):

    valid = set([(y,x) for y,row in enumerate(open(f).read().split('\n')) for x,val in enumerate(row) if val != '#'])
    north = set([(y,x) for y,row in enumerate(open(f).read().split('\n')) for x,val in enumerate(row) if val == '^'])
    south = set([(y,x) for y,row in enumerate(open(f).read().split('\n')) for x,val in enumerate(row) if val == 'v'])
    west  = set([(y,x) for y,row in enumerate(open(f).read().split('\n')) for x,val in enumerate(row) if val == '<']) 
    east  = set([(y,x) for y,row in enumerate(open(f).read().split('\n')) for x,val in enumerate(row) if val == '>'])

    max_y = max(valid)[0]-1
    max_x = max([x[::-1] for x in valid])[0]

    minutes = []
    minute, completed = (0,0)
    terminals = [min(valid),max(valid)]

    queue  = set(terminals[:1])

    while True:

        minute += 1

        north = set([(y-1 if y > 1 else max_y,x) for y,x in north])
        south = set([(y+1 if y < max_y else 1,x) for y,x in south])
        west  = set([(y,x-1 if x > 1 else max_x) for y,x in west])
        east  = set([(y,x+1 if x < max_x else 1) for y,x in east])

        new_queue = set()

        while queue:

            y,x = queue.pop()
            possibilities = [coords for coords in [(y,x),(y-1,x),(y+1,x),(y,x-1),(y,x+1)] if coords in valid]
            new_queue.update([c for c in possibilities if c not in north and c not in south and c not in west and c not in east])

        if terminals[1] in new_queue:

            completed += 1;  minutes += [minute]

            if completed == trips: break
            else:
                terminals = terminals[::-1]
                queue     = set(terminals[:1])          
        else:
            queue = new_queue

    return minutes[0], minutes[-1]
     
print(main('24.txt'))