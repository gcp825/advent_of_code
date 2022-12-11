def main(filepath):

    elves = list(sorted([sum(map(int,x.split('\n'))) for x in open(filepath,'r').read().split('\n\n')]))

    return elves[-1], sum(elves[-3:])
  
print(main('01.txt'))