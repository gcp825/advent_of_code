def next_password(pwd):

    while True:
        
        new = pwd[::-1]        
        for i,x in enumerate(pwd[::-1]):
            if x == 'z':
                new = new[:i] + 'a' + new[i+1:]
            else:
                new = new[:i] + chr(ord(x)+1) + new[i+1:]
                break

        pwd = new[::-1]
        valid = validate(pwd)
        if valid:
            yield pwd

def validate(pwd):
    
    a2z = 'abcdefghijklmnopqrstuvwxyz'
    ones = list('iol')
    twos = [2*x for x in a2z if x not in ones]
    threes = [a2z[i:i+3] for i in range(len(a2z)) if len(a2z[i:i+3].translate(''.maketrans('','',''.join(ones)))) == 3]

    valid = True
    for i in ones:
        if i in pwd:
            valid = False
            break
    if valid:
        valid = False
        for i in range(len(pwd)):
            if pwd[i:i+3] in threes:
                valid = True
                break
    if valid:
        valid = False;  ct = 0;  i = 0
        while i < len(pwd):
            if pwd[i:i+2] in twos:
                i += 1;  ct += 1
                if ct == 2:
                    valid = True
                    break
            i += 1
            
    return valid

def main(start):

    generator = next_password(start)
    pt1 = next(generator)
    pt2 = next(generator)
    
    return pt1, pt2

print(main('cqjxjnds'))
