from collections import deque
from string import ascii_lowercase

def react(polymer):

    polymer = deque([0]+[x if x <= 90 else -(x-32) for x in [ord(x) for x in polymer]])

    while True:

        if polymer[1] == 0: 
            polymer.rotate(-1)
            polymer.popleft()
            break

        if polymer[0] + polymer[1] == 0:
            polymer.popleft()
            polymer.popleft()
            polymer.rotate(1)
        else:
            polymer.rotate(-1)   

    return ''.join([chr(x) if x > 0 else chr(-(x-32)) for x in polymer])

def main(filepath):

    pt1_result  = react(open(filepath,'r').read())
    pt2_results = [len(react(pt1_result.replace(char,'').replace(char.upper(),''))) for char in ascii_lowercase]

    return len(pt1_result), min(pt2_results)

print(main('05.txt'))