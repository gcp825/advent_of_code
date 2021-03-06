#  Golfed! Ish... couldn't resist adding a little structure...

def main(a,z):
             
    p = [min(1,len([x[i:i+2] for i in range(5) if x[i] == x[i+1] and x[i] not in (x[i+2:i+3],x[max(0,i-1):i])]))
            for x in [str(x) for x in range(a,z+1)] if x == ''.join(sorted(x)) and len(set(2*x for x in str(7**18)) & set([x[i:i+2] for i in range(5)])) > 0]

    return len(p),sum(p)

print(main(206938,679128))
