def snafu_to_decimal(n):

    translate = {'0':0,'1':1,'2':2,'-':-1,'=':-2}

    return sum([translate[x]*y for x,y in list(zip(n[::-1],[5**p for p in range(len(n))]))])


def decimal_to_snafu(n):

    translate = {0:'0',1:'1',2:'2',3:'=',4:'-',5:'0'}

    digits = [];  snafu = [];  carry = 0

    while n > 0:

        digits += [n%5]
        n = n//5

    for digit in digits:

        snafu += [translate[digit+carry]]
        carry  = 1 if (digit + carry) > 2 else 0

    return ''.join(snafu)[::-1]


def main(filepath):

    numbers = open(filepath).read().split('\n')

    total = sum([snafu_to_decimal(n) for n in numbers])

    return decimal_to_snafu(total)

     
print(main('25.txt'))