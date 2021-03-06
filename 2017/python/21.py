#  Definitely a challenge to make this one tidy and understandable. About the best I can do... but still don't like a couple of the list (in)comprehensions.

from math import sqrt

def expand_rules(filepath):

    rules = {}
    for src, tgt in [(s.split('/'), t.split('/')) for s,t in [tuple(x.split(' => ')) for x in open(filepath,'r').read().split('\n')]]:
        for _ in range(4):
            rules[tuple(src)] = tgt
            rules[tuple(src[::-1])] = tgt
            src = [''.join([line[i] for line in src])[::-1] for i in range(len(src))]

    return rules

def split(image):

    temp = []
    n = 2 if len(image)%2 == 0 else 3

    for i in range(0,len(image),n): 
        for j in range(0,len(image),n):
            temp += [[image[i+x][j:j+n] for x in range(n)]]

    return temp

def expand(image_list,rules):  
    
    return [rules[tuple(i)] for i in image_list]

def assemble(image_list):

    if len(image_list) == 1: image = image_list[0]
    else:
        image = []
        n = int(sqrt(len(image_list)))
        rows = len(image_list[0])
        for i in range(0,len(image_list),n):
            for r in range(rows):
                image += [''.join([img[r] for img in image_list[i:i+n]])]

    return image

def main(filepath,image,cycles):

    rules = expand_rules(filepath)

    for c in range(cycles):
        image = assemble(expand(split(image),rules))

    return ''.join(image).count('#')

print(main('21.txt',['.#.','..#','###'],5))
print(main('21.txt',['.#.','..#','###'],18))
