#  My original code used translation & comparison of ABC/XYZ in Part 2 to calculate the round score. This refactored version uses 
#  an index adjustment to return the appropiate score from the scores dict; it's the structure of the dictionary that really makes it work.

def main(f):

    scores = {'A':'483','B':'159','C':'726'}

    score = lambda a,b,part: int(scores[a][((ord(b)-88)+((ord(a)-66)*(part-1)))%3])

    return tuple(map(sum,zip(*[(score(*round,1),score(*round,2)) for round in [line.split(' ') for line in open(f).read().split('\n')]])))

print(main('02.txt'))