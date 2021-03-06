def main(filepath):
    
    rows = [[int(x[0:5].strip()), int(x[5:10].strip()), int(x[10:15].strip())] for x in [x for x in open(filepath,'r').read().split('\n')]]
    vals = [x[0] for x in rows] + [x[1] for x in rows] + [x[2] for x in rows]
    cols = [vals[i:i+3] for i in range(0,len(vals),3)]

    return sum([1 for x in rows if sum(x)-max(x) > max(x)]), sum([1 for x in cols if sum(x)-max(x) > max(x)])

print(main('03.txt'))
