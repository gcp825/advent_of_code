def read_file(filepath):
    
    with open(filepath,'r') as i:
        presents = [sorted([int(x[0]),int(x[1]),int(x[2])]) for x in [x.split('x') for x in [x for x in i.read().split('\n')]]]
    return presents

def calculate(presents,wrapping=0,ribbon=0):
    
    for gift in presents:
        wrapping += (lambda d: (3*d[0]*d[1])+(2*d[0]*d[2])+(2*d[1]*d[2])) (gift)
        ribbon   += (lambda d: (2*d[0])+(2*d[1])+(d[0]*d[1]*d[2]))        (gift)
    return wrapping, ribbon
        
def main(filepath):
    
    wrapping, ribbon = calculate(read_file(filepath))
    return wrapping, ribbon

print(main('2.txt'))

