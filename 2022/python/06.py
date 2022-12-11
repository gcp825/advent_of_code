def locator(input,n): 
    
    return [i for i in range(n,len(input)+1) if len(list(set(input[i-n:i]))) == n][0]

print((locator(open('06.txt').read(),4),locator(open('06.txt').read(),14)))