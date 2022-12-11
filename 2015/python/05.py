def read_file(filepath):
    
    with open(filepath,'r') as f:        
       data = f.read().split('\n')
    return data

def validator(data,ruleset,vowel_ct=3,repeat_ct=2,invalid_str=['ab','cd','pq','xy']):
    
    valid_ct = 0
    for string in data:
        if ruleset == 1:
            valid_ct += (1 if validate_v1(string,vowel_ct,repeat_ct,invalid_str) is True else 0)
        if ruleset == 2:
            valid_ct += (1 if validate_v2(string,repeat_ct) is True else 0)        
    return valid_ct        

def validate_v1(string,vowel_ct,repeat_ct,invalid_str):

    valid = True;  length = len(string)
    
    if any(x in string for x in invalid_str): valid = False
        
    if valid and len(string.translate(''.maketrans('','','aeiou'))) + vowel_ct > length: valid = False
        
    if valid:                                          # regex alternative: re.search(r'([a-z])\1', string)
        for i,c in enumerate(string):
            if len(string[i:i+repeat_ct].replace(c,'')) == 0: break
        if i > length-repeat_ct: valid = False

    return valid

def validate_v2(string,repeat_ct):

    valid = False;  length = len(string); i = 0
    
    while not valid and i < length:                    # regex alternative: re.findall(r'([a-z]{2}).*\1', string)             
        if string[i+repeat_ct:].find(string[i:i+repeat_ct]) >= 0: valid = True
        i += 1
 
    if valid:                                          # regex alternative: re.findall(r"([a-z]).\1", string)                                        
        valid = False;  i = 0
        while not valid and i < length:
            if string[i:i+1] == string[i+2:i+3]: valid = True
            i += 1
       
    return valid
            
def main(filepath,ruleset):
    
    return validator(read_file(filepath),ruleset)
        
print(main('5.txt',1))
print(main('5.txt',2))
