#  A scrappy quickly knocked together bit of code, just because it felt like I should have some code for this puzzle. Basically a like-for-like 
#  automation of my manual solve approach (except that it's generating all valid numbers using that method rather than just min and max).

def main(filepath):

    d1 = [(i,tuple(enumerate(x.split('\n')))) for i,x in enumerate(open(filepath,'r').read().replace('\ninp','\n\ninp').split('\n\n'))]
    d2 = [(i,*[int(v[n][-1].split(' ')[-1]) for n in (4,5,15)]) for i,v in d1]
    d3 = [(a[0],b[0],a[3]+b[2]) for a in d2 for b in d2 if b[0] == a[0]+1 and a[1] < b[1]]
    d4 = [x for x in d2 if x[0] not in [a[0] for a in d3]+[a[1] for a in d3]]
    d5 = [(a[0],b[0],a[3]+b[2]) for i,a in enumerate(d4[:len(d4)//2]) for j,b in enumerate(d4[len(d4)//2:][::-1]) if i == j]

    digits = len(d1);  valid_digits = ['']*digits;  valid_numbers = [['']*14]

    rules = list(sorted(d3+d5))

    get_digits = lambda x: ([str(n) for n in range(1,10) if 0 < x+n <= 9], [str(x + n) for n in range(1,10) if 0 < x+n <= 9])

    for i,j,n in rules:
        valid_digits[i], valid_digits[j] = get_digits(n)

    for a,b,_ in rules:
        new_numbers = []
        for nbr in valid_numbers:
            for i,n in enumerate(valid_digits[a]):
                new_number = [] + nbr
                new_number[a] = n
                new_number[b] = valid_digits[b][i]
                new_numbers += [new_number]
        valid_numbers = new_numbers

    valid_numbers = [int(''.join(x)) for x in valid_numbers]

    print(len(valid_numbers),'valid numbers. Max and Min:')

    return valid_numbers[-1], valid_numbers[0]
         
print(main('24.txt'))