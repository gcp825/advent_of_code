#  Enjoyed this one. Basic string manipulation approach of finding the innermost set of parentheses, replacing those and the calculation within with it's
#  result and then keep working outwards until left with a calculationm without any parentheses. That can then be split into lists of numbers and operators
#  that can then be applied to each other sequentially. Similar approach with pt2 except that instead of looking for parentheses you look for the
#  operator you want to elevate, calculate the result of those calculations first and replace with their respective results in the string before processing
#  as per Part 1.

#  Didn't just limit myself to the input on this one either: it should cope with any postive integers of any length and elevations of any and/or multiple
#  operators. Would need some minor tweaking for negative integers and exponentials.

def read_file(filepath):
    
    with open(filepath,'r') as f:
        
        calcs = ['(' + x.replace(' ','') + ')' for x in f.read().split('\n')]
                
    return calcs


def process_calcs(calcs,elevations=''):
  
    total = 0
    for calc in calcs:
        total += calculate(calc,elevations)
        
    return total
    

def calculate(c,elevations):
    
    a = '('
    z = ')'

    while c.count(a) > 0:

        new_c = '';  i = 0
  
        while i < len(c):    
            if c[i] == a:                                     #  if current byte is an opening parenthesis             
                x = c[i+1:].find(z)+i+1                       #    find next closing parenthesis
                if x < (c[i+1:]+a).find(a)+i+1:               #  if index of closing parenthesis < index of next opening parenthesis
                    new_c += resolve(c[i+1:x],elevations)     #    then resolve the contents of the parentheses and replace with the result
                    i = x
                else:
                    new_c += c[i]
            else:
                new_c += c[i]
            i += 1
        c = new_c
        
    return int(c)


def resolve(c,elevations):
    
    for op in [x for x in elevations if x in list('*/+-')]: c = elevate(c,op)       
    
    values = [int(x) for x in c.translate(c.maketrans('/+-','***','')).split('*')]
    op = [''] + list(c.translate(c.maketrans('','','0123456789')))

    result = values[0]
    for i,v in enumerate(values):
        if i > 0: result = eval(str(result)+ op[i] + str(v))
   
    return str(result)


def elevate(c,op):
    
    repl = c.maketrans('*/+-','****','');
    s = '*'
    
    while c.count(op) > 0:
        
        i = c.find(op)
        start = i - (c[0:i].translate(repl)[::-1]+s).find(s)
        end = len(c[i+1:].translate(repl).split(s)[0]) + i + 1
        
        c = c[0:start] + str(eval(c[start:end])) + c[end:]

    return c

      
def main(filepath):
    
    pt1 = process_calcs(read_file(filepath))
    pt2 = process_calcs(read_file(filepath),'+')
    
    return pt1, pt2
        
print(main('18.txt'))
