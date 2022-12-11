def main(filepath,decrease):

    offsets = list(map(int,open(filepath,'r').read().split('\n')))
    steps = 0;  i = 0;  z = len(offsets)-1

    while 0 <= i <= z:
        jump = offsets[i]
        offsets[i] = jump-1 if decrease and jump >= 3 else jump+1
        i += jump
        steps += 1        

    return steps

print(main('05.txt',False))
print(main('05.txt',True))
