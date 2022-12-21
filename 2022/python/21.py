def monkey_business(numbers,sums,part2=False):

    numbers = {**numbers}
    sums    = [] + sums

    if type(part2) is int: 
        numbers['humn'] = part2

    while sums:

        remaining = []

        for sum, num_1, num_2, op in sums:

            if num_1 in numbers and num_2 in numbers:

                one = numbers[num_1]
                two = numbers[num_2]

                if sum == 'root' and type(part2) is int:
                    numbers[sum] = two-one
                    remaining = []
                else:
                    result = (one + two) if op == '+' else (one - two) if op == '-' else (one * two) if op == '*' else (one // two)
                    numbers[sum] = result
            else:
                remaining += [(sum,num_1,num_2,op)]

        sums = remaining

    return numbers['root']


def binary_search(numbers,sums):

    a = monkey_business(numbers,sums,0)
    b = monkey_business(numbers,sums,abs(a))
    t = 1

    while t != 0:

        s = (a+b)//2
        t = monkey_business(numbers,sums,s)
        a = s if t < 0 else a
        b = s if t > 0 else b

    while t == 0:
        s -= 1
        t = monkey_business(numbers,sums,s)

    return s+1


def main(filepath):

    numbers = dict([(k,int(v)) for k,v in [tuple(x.split(': ')) for x in open(filepath).read().split('\n')] if v.isnumeric()])
    sums    = [(k,v[:4],v[7:11],v[5]) for k,v in [tuple(x.split(': ')) for x in open(filepath).read().split('\n')] if not v.isnumeric()]

    pt1 = monkey_business(numbers,sums)
    pt2 = binary_search(numbers,sums)

    return pt1, pt2

print(main('21.txt'))