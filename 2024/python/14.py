import re

def simulate(robots, seconds, w, h):

    return [(vy, vy, (y+(vy*seconds)) % h, (x+(vx*seconds)) % w) for vy,vx,y,x in robots]


def calculate_safety_factor(robots, w, h):

    q1 = sum(1 for _,_,y,x in robots if 0 <= y < h//2 and 0 <= x < w//2)
    q2 = sum(1 for _,_,y,x in robots if 0 <= y < h//2 and w//2 + w%2 <= x < w)
    q3 = sum(1 for _,_,y,x in robots if h//2 + h%2 <= y < h and 0 <= x < w//2)
    q4 = sum(1 for _,_,y,x in robots if h//2 + h%2 <= y < h and w//2 + w%2 <= x < w)

    return q1*q2*q3*q4


def easter_egg_hunt(robots, w, h):
    ''' Counts robots in the centre portion of the grid and returns the seconds value with the highest robot count'''

    distinct_states = w*h
    best_so_far = (0, -1)

    for seconds in range(1, distinct_states):
        score = sum(1 for r in simulate(robots, seconds, w, h) if h//4 <= r[2] <= (h//4)*3 and w//4 <= r[3] <= (w//4)*3)
        if score > best_so_far[0]:
            best_so_far = (score, seconds)

    return best_so_far[1]


def render(robots):

    coords = [r[2:] for r in robots]

    for y in range(max(r[0] for r in coords)):
        line = ''
        for x in range(max(r[1] for r in coords)):
            line += '*' if (y,x) in coords else '.'
        print(line)


def main(filepath, w=101, h=103):

    robots = [tuple(map(int,re.findall('-?\d+',line)))[::-1] for line in open(filepath).read().split('\n')]

    safety_factor = calculate_safety_factor(simulate(robots,100,w,h),w,h)

    seconds = easter_egg_hunt(robots,w,h)
    render(simulate(robots,seconds,w,h))

    return safety_factor, seconds


print(main('14.txt'))