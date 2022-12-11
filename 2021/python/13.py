def parse_file(f):

    input = [tuple(x.split(',')) for x in open(f,'r').read().replace('fold along ','').replace('=',',').replace('\n\n','\n').split('\n')]

    return [((int(x),int(y)),chr(0x2588)) for x,y in input if x.isnumeric()], [(x,int(y)) for x,y in input if not x.isnumeric()]

def fold(paper,fold_type,fold_at):

    folds = {'x':0,'y':1}
    adjust = lambda coord, fold_type, fold_at, x_or_y: fold_at + (fold_at - coord) if x_or_y == fold_type else coord

    keep      = [(coords,dot) for coords, dot in paper if coords[folds[fold_type]] < fold_at]
    transpose = [((adjust(coords[0],fold_type,fold_at,'x'), 
                   adjust(coords[1],fold_type,fold_at,'y')),dot) for coords, dot in paper if coords[folds[fold_type]] > fold_at]

    return list(set(keep+transpose))

def render(paper):

    dots = dict(paper);  coords = dots.keys()

    x,xx = (min(coords)[0], max(coords)[0]+1)
    y,yy = (min(c[::-1] for c in coords)[0], max(c[::-1] for c in coords)[0]+1)

    print('\n')

    for row in range(min(0,y),yy):
        line = ''
        for col in range(min(0,x),xx):
            line += dots.get((col,row),' ')
        print(line)

    return '\n'     
    

def main(filepath):

    paper, folds = parse_file(filepath)    
    
    for i, instr in enumerate(folds): 
        paper = fold(paper,*instr)
        if i == 0: print('Part 1:', len(paper), '\n')

    print('Part 2:')
    
    return render(paper)
    
print(main('13.txt'))