import re

def simulate(robots, seconds, w, h):

    return [(vy, vy, (y+(vy*seconds)) % h, (x+(vx*seconds)) % w) for vy,vx,y,x in robots]


def calculate_safety_factor(robots, w, h):

    q1 = sum(1 for _,_,y,x in robots if 0 <= y < h//2 and 0 <= x < w//2)
    q2 = sum(1 for _,_,y,x in robots if 0 <= y < h//2 and w//2 + w%2 <= x < w)
    q3 = sum(1 for _,_,y,x in robots if h//2 + h%2 <= y < h and 0 <= x < w//2)
    q4 = sum(1 for _,_,y,x in robots if h//2 + h%2 <= y < h and w//2 + w%2 <= x < w)

    return q1*q2*q3*q4


def render(robots):

    coords = [r[2:] for r in robots]

    for y in range(max(r[0] for r in coords)):
        line = ''
        for x in range(max(r[1] for r in coords)):
            line += '*' if (y,x) in coords else '.'
        print(line)


def main(filepath, w=101, h=103):

    robots = [tuple(map(int,re.findall('-?\d+',line)))[::-1] for line in open(filepath).read().split('\n')]
    lowest = float("inf")

    for seconds in range(w*h):
        safety_factor = calculate_safety_factor(simulate(robots,seconds,w,h),w,h)
        if seconds == 100:
            part_1 = safety_factor
        if safety_factor < lowest:
            lowest = safety_factor
            part_2 = seconds

    render(simulate(robots,part_2,w,h))

    return part_1, part_2


print(main('14.txt'))