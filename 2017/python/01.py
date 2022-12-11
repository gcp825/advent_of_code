from itertools import groupby

def pt1_captcha(inp): return sum([x*y for x,y in [(int(x),len(list(y))-1) for x,y in groupby(inp+inp[0])] if y > 0]) 
def pt2_captcha(inp): return sum([int(x)+int(y) for x,y in [(inp[i],inp[i+(len(inp)//2)]) for i in range(len(inp)//2)] if x == y])

def main(filepath):

    inp = open(filepath,'r').read().strip('\n')
    return pt1_captcha(inp), pt2_captcha(inp)

print(main('01.txt'))
