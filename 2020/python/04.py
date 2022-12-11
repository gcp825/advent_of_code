# Old School Read-Ahead procedural file processing approach

from functools import reduce
from operator  import concat

def parse_attributes(x):
    return x.split(' ') if len(x) > 0 else None

def valid_pattern(x,patterns):
    return True if reduce(concat,sorted([a.split(':')[0] for a in x])) in patterns else False

def validate_fields(x):

    # cutting some corners with the hard-coding
 
    valid = True
 
    for attr in x:
        
        k,v = attr.split(':')
        
        if ((k == 'byr' and v.isnumeric() and 1920 <= int(v) <= 2002)
        or  (k == 'iyr' and v.isnumeric() and 2010 <= int(v) <= 2020)
        or  (k == 'eyr' and v.isnumeric() and 2020 <= int(v) <= 2030)
        or  (k == 'hgt' and v[:-2].isnumeric() and v[-2:] == 'cm' and 150 <= int(v[:-2]) <= 193)
        or  (k == 'hgt' and v[:-2].isnumeric() and v[-2:] == 'in' and 59 <= int(v[:-2]) <= 76)
        or  (k == 'hcl' and len(v) == 7 and v[0:1] == '#' and len(v[1:].translate(v.maketrans('','','abcdef0123456789'))) == 0)
        or  (k == 'ecl' and v in ('amb','blu','brn','gry','grn','hzl','oth'))
        or  (k == 'pid' and len(v) == 9 and v.isnumeric())
        or  (k == 'cid')):
            continue
        else:
            valid = False
            break
        
    return valid

def validate_passport(x,patterns,mode):

    y = valid_pattern(x,patterns)
    if mode == 1 or y is False:
        return y
    else:
        return validate_fields(x)    
    
def process_passports(filepath,val_mode):
    
    with open(filepath,'r') as passports:
    
        attributes = []
        valid_ct = 0
        valid_patterns = ['byrcidecleyrhclhgtiyrpid','byrecleyrhclhgtiyrpid']
    
        for line in passports:
 
            # extract any new attributes
            x = line[:-1] if len(line) > 0 and line[-1] == "\n" else line
            new_attributes = parse_attributes(x)
 
            # if no new attributes to add to the current passport, we can validate it and move on to the next line
            if new_attributes is None:   
                if validate_passport(attributes,valid_patterns,val_mode) is True: valid_ct += 1
                attributes = []
            # else add the new attributes to the list for the current passport and move on to the next line
            else:
                attributes = attributes + new_attributes
                
        else:
           # Validate the final passport in the file
           # (as we don't know the attribute list for the final passport is complete until the for loop is exhausted)
            if validate_passport(attributes,valid_patterns,val_mode) is True: valid_ct += 1
        
    return valid_ct
    
print(process_passports('passports.txt',1))  # part 1
print(process_passports('passports.txt',2))  # part 2
      
