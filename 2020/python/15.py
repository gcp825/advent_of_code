def main(seq,tgt): 
    
    numbers = {}    
    for i,n in enumerate(seq[:-1]): numbers[n] = i+1
        
    last = seq[-1]; i+=3

    while i <= tgt:
         
        this = i-1-numbers[last] if last in numbers else 0
        numbers[last] = i-1 
        last = this; i+=1
    
    return last

print('pt1:',main([20,0,1,11,6,3],2020))
print('pt2:',main([20,0,1,11,6,3],30000000))
