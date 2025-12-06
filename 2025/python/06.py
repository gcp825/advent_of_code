from functools import reduce
from operator import add, mul

def parse_input(f):

    data = open(f).read().split('\n')
    delimiter_positions = [i for i,x in enumerate(data[-1].replace(' +',',+').replace(' *',',*')) if x == ',']
    delimited = [''.join(',' if i in delimiter_positions else x for i,x in enumerate(line)) for line in data]
    calculations = [[{'+':add,'*':mul}.get(x.strip(),x) for x in line.split(',')] for line in delimited]

    return read_top_to_bottom(calculations)


def read_top_to_bottom(calculations):

    return [[row[i] for row in calculations] for i in range(len(calculations[0]))]


def read_right_to_left(numbers):

    return [int(''.join(num[i:i+1] for num in numbers)) for i in range(len(str(max(map(int,numbers)))))]


def main(filepath):

    calculations = [(x[-1],x[:-1]) for x in parse_input(filepath)]
    transform = {1: lambda x: [int(n) for n in x], 2: read_right_to_left}

    return tuple(sum(reduce(op,transform[pt](numbers)) for op, numbers in calculations) for pt in (1,2))


print(main('06.txt'))