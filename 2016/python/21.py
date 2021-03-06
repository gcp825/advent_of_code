from enhancements import replace_

def swap_position(s,x,y):  return s[:x] + s[y] + s[x+1:y] + s[x] + s[y+1:]                     

def swap_letter(s,x,y):    return s.translate(''.maketrans(x+y,y+x,''))               

def rotate_left(s,x):      return s[x%len(s):] + s[:x%len(s)]                                  

def rotate_right(s,x):     return s[(x%len(s))*-1:] + s[:(x%len(s))*-1]                                 

def rotate_on_x(s,x):      return rotate_right(s,1+s.find(x)+min(s.find(x)//4,1))

def unrotate_on_x(s,x):    return [rotate_right(s,x[0]) for x in [(i,rotate_on_x(rotate_right(s,i),x)) for i in range(len(s))] if x[1] == s][0]

def reverse(s,x,y):        return s[:x] + s[x:y+1][::-1] + s[y+1:]

def move(s,x,y):           s = list(s);  s.insert(y,s.pop(x));  return ''.join(s)   

def parse(filepath,unscramble=False):

    instr = [(x[0],min(x[1],x[2]),max(x[1],x[2])) if x[0] == 'swap_position' else x for x in
              [tuple(replace_(x,['based on position of letter','rotate ','swap ','with letter ','with position ',' steps',' step','positions ','through ','to ',' position'], 
                                ['on_x','rotate_','swap_','']).split(' ')) 
                                    for x in open(filepath,'r').read().split('\n')]]

    if unscramble:

        instr = [(x[0],x[2],x[1])                                                                                        if x[0] == 'move' else
                 (x[0],min(x[1],x[2]),max(x[1],x[2]))                                                                    if x[0] == 'swap_position' else
                 (replace_(x[0],['left','right','rotate_on','_l','_r'],['r','l','unrotate_on','_left','_right']),x[1])   if x[0].startswith('rotate') else
                  x for x in instr[::-1]]

    return instr


def process(instr,pwd):
 
    for func, p1, *p2 in instr:

        p2 = list(p2+[''])[0];  
        qt = "'" if func.startswith(('swap_letter','rotate_on','unrotate_on')) else ''

        pwd = eval(func + '(' + "'" + pwd + "'" + ',' + qt+p1+qt + ('' if len(p2) == 0 else ',' + qt+p2+qt) + ')')

    return pwd
    

def main(filepath):

    pt1 = process(parse(filepath),'abcdefgh')
    pt2 = process(parse(filepath,True),'fbgdceah')

    return pt1, pt2

print(main('21.txt'))
