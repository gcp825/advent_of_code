#  Kind of a math-y brute force solution

from math import sqrt

def divisors(n):
    
    a = [i for i in range(1,int(sqrt(n))+1) if n % i == 0]     #  didn't bother working out how to get divisors... just googled it and
    b = [int(n/d) for d in a if n != d*d]                      #  adapted a generator solution from stackoverflow into list comprehension                
    return a+b

def main(n):
    
    pt1=0; pt2=0
    
    for i in range(int(n/50)-int(n/50)%6, n, 6):               #  Found pt1 answer by experimenting with ranges of 100000 rather than iterating from 0
        d1 = divisors(i)                                       #  Converted range start point to a formula such that it can vary with the input.
        d2 = [d for d in d1 if i/d <= 50]                      #  Strides every 6th value as the integer sequence (number of presents) spikes
        if pt1 == 0 and sum(d1)*10 > n: pt1 = i                #  significantly every 6th value and never surpasses that until the next spike; thus the 
        if pt2 == 0 and sum(d2)*11 > n: pt2 = i                #  correct answer will be divisible by 6.
        if min(pt1,pt2) > 0: break
        
    return pt1, pt2

print(main(29000000))
