def main(filepath):
    
    freqs = [int(x) for x in open(filepath,'r').read().split('\n')]
    
    seen = set([0]);  freq, ct = (0,1)

    while len(seen) == ct:
        for f in freqs:
            freq += f;  ct += 1
            if freq in seen: break
            seen.add(freq)

    return (sum(freqs), freq)        
  
print(main('01.txt'))