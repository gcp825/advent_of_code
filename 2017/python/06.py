def main(filepath):

    banks = list(map(int,open(filepath,'r').read().strip('\n').split('\t'))) 
    config = ''.join([chr(ord('a')+b) for b in banks])   
    cycles = 0;  configurations = {};   bank_ct = len(banks) 
    
    while config not in configurations.keys():
        configurations[config] = cycles
        i = min(i for i,b in enumerate(banks) if b == max(banks))
        redist, banks[i] = banks[i], 0
        while redist > 0:
            i = (i+1) % bank_ct
            banks[i] += 1
            redist -= 1
        config = ''.join([chr(ord('a')+b) for b in banks])
        cycles += 1

    return cycles, cycles-configurations[config]

print(main('06.txt'))
