def main(filepath):
    
    with open(filepath,'r') as f:
        x = f.read().split('\n')
        pt1 = sum(len(x) - len(eval(x)) for x in x)
        pt2 = sum(4 + x[1:-1].count('\\') + x[1:-1].count('"') for x in x)
        
    return (pt1,pt2)

print(main('8.txt'))
