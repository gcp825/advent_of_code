#  Nothing to see here.

from itertools import product

def main(filepath):
    
    addr = [x.split('[') for x in open(filepath,'r').read().replace(']','[').split('\n')]
    az   = list('abcdefghijklmnopqrstuvwxyz')    
    abba = [(''.join(x))+(''.join(x)[::-1]) for x in list(product(az,az)) if x[0] != x[1]]
    aba  = [x[0:2]+x[3:4] for x in abba]

    tls = 0;  ssl = 0
    for a in addr:
        
        tls_valid = False;  ssl_valid = False;  bab = []
        
        for i in range(0,len(a),2):
            if not tls_valid:
                for x in abba:
                    if x in a[i]:
                        tls_valid = True
                        break
            for x in aba:
                if x in a[i]:
                    ssl_valid = True
                    bab += [x[1:3]+x[1]]

        bab_ct = 0
        for i in range(1,len(a),2):
            if tls_valid:
                for x in abba:
                    if x in a[i]:
                        tls_valid = False
                        break
            if ssl_valid and bab_ct == 0:
                for x in bab:
                    if x in a[i]:
                        bab_ct = 1
                        break
          
        if tls_valid:  tls += 1
        if bab_ct > 0: ssl += 1
                        
    return tls, ssl

print(main('07.txt'))
