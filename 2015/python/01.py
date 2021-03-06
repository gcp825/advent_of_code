def read_file(filepath):
    
    with open(filepath,'r') as i:
        inst = [int(x) for x in i.read().replace(')','-1,').replace('(','1,').strip('\n').strip(',').split(',')]
    return inst

def calculate(inst,floor=0):
    
    for i,f in enumerate(inst):
        floor += f
        if floor < 0: break
        
    return sum(inst), i+1
        
def main(filepath):
    
    pt1, pt2 = calculate(read_file(filepath))
    return pt1, pt2    

print(main('1.txt'))
