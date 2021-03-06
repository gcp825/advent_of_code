#  Another one where my aversion to recursion resulted in spending far too long trying to come up with a pure maths solution for Part 2 
#  (and as ever, nearly getting there but ultimately failing). The original Part 1 where I fully decompress the file just got scrapped
#  in favour of adding a simple if part 2 else... path to the Part 2 solution.

def decompress(file,full_decompress=True):

    i = 0;  length = 0
        
    while i < len(file):
        
        if file[i] == '(':
            
            rule_start = i + 1;  rule_end = file[rule_start:].find(')') + rule_start;  chunk_start = rule_end + 1
            
            chunk_length, repeat = ([int(x) for x in file[rule_start:rule_end].split('x')])
            
            i = chunk_start + chunk_length             #  increment i to the character in the file following the chunk we need to decompress
            
            if full_decompress:
                chunk = file[chunk_start:i]            #  isolate the chunk of the file to decompress
                length += decompress(chunk) * repeat   #  recursively calculate the length of that chunk
            else:
                length += chunk_length * repeat        #  calculate length of the chunk after first decompression only
            
        else:
            
            length += 1;  i += 1                       #  not part of a rule or compressed chunk so count as length 1 and move on

    return length


def main(filepath):
    
    f = open(filepath,'r').read()
    pt1 = decompress(f,False)
    pt2 = decompress(f,True)
    
    return pt1, pt2    


print(main('09.txt'))
