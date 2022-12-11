# I know this one has a load of much more elegant solutions out there... I even toyed with a different one myself... but based on the actual data
# (yeah, yeah, I know...) I just went basic, ugly, repetitive BRUTE FORCE as a time saving measure (mine rather than CPU!)

# The exec/eval in Pt 1 (just because the addr string in the input is in the exact format required to update a Python dict) is ridiculous.


def read_file(filepath):
    
    with open(filepath,'r') as f:
        
        a = [x.split(' = ') for x in [x for x in f.read().split('\n')]]
        b = [(x[0],int(x[1]) if x[0] != 'mask' else x[1]) for x in a]

    return b


def format_mask(raw_mask,ignore):
    
    mask = []
    for i,v in enumerate(list(raw_mask)):
        if v != ignore: mask += [(i,v)]
        
    return mask


def v1_decoder(instr):
    
    dict_nm = instr[1][0].split('[')[0]
    exec(dict_nm + ' = {}')
    
    for a,b in instr:
        
        if a == 'mask':
            mask = format_mask(b,'X')
            length = len(b)
        else:
            upd = str(format(b,'b')).rjust(length,'0')
            for i,r in mask:
                upd = ''.join(list(upd)[0:i] + [r] + list(upd)[i+1:])
            
            exec(a + ' = ' + str(int(upd,2)))
        
    return eval(dict_nm)

    
def v2_decoder(instr):
    
    mem = {}

    for a,b in instr:
       
        if a == 'mask':

            mask = format_mask(b,'0')
            length= len(b)
            
        else:
            
            addr = str(format(int(a[a.find('[')+1:a.find(']')]),'b')).rjust(length,'0')

            for i,r in mask:
                addr = ''.join(list(addr)[0:i] + [r] + list(addr)[i+1:])
                if r == 'X': tgt = i
                
            stash = [] + [addr]
            i = 0
                    
            while i <= tgt:
                
                if i < tgt and addr[i] == 'X':
                    new_stash = []
                    for s in stash:
                        new_stash += [''.join(list(s)[0:i] + ['0'] + list(s)[i+1:])]
                        new_stash += [''.join(list(s)[0:i] + ['1'] + list(s)[i+1:])]
                    stash = [] + new_stash
                
                if i == tgt:
                    for s in stash:
                        mem[int(''.join(list(s)[0:i] + ['0'] + list(s)[i+1:]),2)] = b
                        mem[int(''.join(list(s)[0:i] + ['1'] + list(s)[i+1:]),2)] = b
                        
                i += 1
   
    return mem
    
    
def main(filepath):
    
     instructions = read_file(filepath)
     pt1 = v1_decoder(instructions)
     pt2 = v2_decoder(instructions)

     return sum(pt1.values()), sum(pt2.values())

    
print(main('14.txt'))
