#  Part 1 annoyed me. Maybe it would have been too simple without the 'trick', but not all Part 1's are very difficult... Part 2 is typically 
#  where it ramps up. And for that matter Day 17 was simply brute-forcible for both parts and that was only 3 days ago. 
#  So I wasn't prepared for it, and I'm not sure I would have spotted it (at least not without a massive amount of frustration first) without 
#  the hints on the work slack channel. 
#  Other than that, it's pretty straightforward and optimised to just store lit values only. Still pretty slow... but it is python.

def parse_file(filepath):

    algo, image = tuple([x for x in open(filepath,'r').read().split('\n\n')])

    return list(algo), set([(y,x) for y,row in enumerate([list(x) for x in image.split('\n')]) for x,val in enumerate(row) if val == '#'])

def main(filepath,cycles=50):

    algo, image = parse_file(filepath);  lit = [len(image)]

    pixel = lambda y,x: '1' if (y,x) in image else '0' if 0 <= y < max_y and 0 <= x < max_x else default

    for n in range(1,cycles+1):

        max_y = max(image)[0]+1
        max_x = max([i[::-1] for i in image])[0]+1

        default = '1' if n%2 == 0 and algo[0] == '#' else '0'

        image = set([(y+1,x+1) for y in range(-1,max_y+1) for x in range(-1,max_y+1) 
                               if algo[int(''.join([pixel(yy,xx) for yy in range(y-1,y+2) for xx in range(x-1,x+2)]),2)] == '#'])

        lit += [len(image)]

    return lit[2], lit[50]

print(main('20.txt'))