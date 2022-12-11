from collections import Counter

def pwd_valid(mode, char, pwd, x, y):
    
    if mode == 1:
        p = pwd
        
    if mode == 2:
        p = pwd[x-1:x] + pwd[y-1:y]
        x,y = 1,1
        
    count = Counter([x for x in p])
    
    if x <= count[char] <= y:
        return True
    else:
        return False 
    
def validator(mode,pwd_list):
    
    valid_ct = 0
    
    for p in pwd_list:
        
        char = p.split(':')[0][-1:]
        pwd = p[::-1].split(' ')[0][::-1]
        x = int(p.split('-')[0])
        y = int(p.split('-')[1].split(' ')[0])
        
        if pwd_valid(mode,char,pwd,x,y) is True: valid_ct += 1
    
    return valid_ct
            
pwds = ['1-3 a: abcde', '1-3 b: cdefg', '2-9 c: ccccccccc']

print(validator(1,pwds))  # part 1
print(validator(2,pwds))  # part 2
