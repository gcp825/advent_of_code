# Old School Read-Ahead procedural file processing approach

from collections import Counter

def get_yes_answers(x):
    
    def count_yes(x,y): return len(y) - len(y.translate(x.maketrans('','',x)))   
    
    y = 'abcdefghijklmnopqrstuvwxyz'
     
    d = Counter([a for a in x])
    z = ''.join([k for k,v in d.items() if k != '#' and v == d['#']])  # distinct q's answered yes by all
    
    return (count_yes(x,y), count_yes(z,y))


def process_answers(filepath):
    
    with open(filepath,'r') as answers:
    
        a = ''; ct = (0,0)
    
        for line in answers:
 
            if line[0:1] == '\n':
                ct = tuple(map(sum,zip(ct,get_yes_answers(a))))  #  increment both counts with zip and map/sum to recreate the ct tuple
                a = ''
            
            else: a += ('#' + line.replace('\n',''))

        else: ct = tuple(map(sum,zip(ct,get_yes_answers(a))))    #  ensure we cater for the final group of answers when for loop exhausted 
        
    return ct
    
    
print(process_answers('answers.txt'))  # parts 1 & 2
      
