from collections import Counter

def read_file(filepath):
    
    with open(filepath,'r') as f:
        
        a = [x for x in f.read().split('\n\n')]
        
        b = []; d = []
        
        for x in [[x[0],x[1].split(' or ')] for x in [x.split(': ') for x in a[0].split('\n')]]:
            for y in x[1]:
                z = y.split('-')
                b += [[x[0],range(int(z[0]),int(z[1])+1)]]
                
        c = [int(x) for x in [x for x in a[1].split('\n')][1].split(',')]

        for x in a[2].split('\n')[1:]:
            d += [[int(x) for x in x.split(',')]]
          
    return b,c,d


def validate_tix(tix,rules):
    
    valid_tix = []; error_rate = 0
    
    for t in tix:
        
        curr_rate = error_rate
        
        for n in t:
            valid = False
            for r in rules:
                if n in r[1]:
                    valid = True
                    break
            if not valid: error_rate += n
                
        if curr_rate == error_rate: valid_tix += [t]
    
    return valid_tix, error_rate


def determine_fields(tix,rules):
    
    fields = list(map(list,zip(*tix)))
    length = len(rules)
    results = {}; p = []
    
    for e,f in enumerate(fields):
        
        i = 0
        while i < length:
            
            valid = []
            for r in rules[i:i+2]:
                for n in f:
                    if n in r[1]: valid += [n]
                    
            if sorted(f) == sorted(valid): p += [(r[0],str(e))]
            i += 2
    
    while len(p) > 0:
        
        count = Counter([x[0] for x in p])
        matches = [x for x in p if x[0] in [k for k,v in count.items() if v == 1]]
        
        for a,b in matches:
            results[a] = int(b)
            p = [x for x in p if x[1] != b]
                
    return results


def check_ticket(my_ticket,fields):

    total = 0
    for k,v in fields.items():
        if k[0:9] == 'departure':
            total = max(total,1) * my_ticket[v]
        
    return total

            
def main(filepath):
    
     rules, my_ticket, tickets = read_file(filepath)
     valid_tickets, pt1        = validate_tix(tickets,rules)
     fields                    = determine_fields(valid_tickets,rules)
     pt2                       = check_ticket(my_ticket,fields)
     
     return pt1, pt2
     
         
print(main('day16.txt'))
