def parse_input(filepath):

    input1, input2 = [(x,y.split('\n')) for x,y in [tuple(open(filepath).read().split('\n\n'))]][0]

    directions = input1.replace('L','0').replace('R','1')
    nodes = dict([(x[0:3],(x[3:6],x[6:9])) for x in [''.join([y for y in z if y.isalnum()]) for z in input2]])

    return directions, nodes


def lcm(numbers):

    '''Returns the Least Common Multiple from a supplied list of numbers'''

    gcd  = lambda a,b: a if b == 0 else gcd(b,a % b)
    nums = list(sorted(list(set(numbers))))[::-1]

    while len(nums) > 1:
        nums = [(nums[0]*nums[1]) // gcd(nums[0],nums[1])] + nums[2:] 

    return nums[0]


def travel(directions, nodes, location='AAA', destination='ZZZ', steps=0):

    wrap = len(directions)
    destinations = [n for n in nodes.keys() if n.endswith(destination)]

    while location not in destinations:
        direction = int(directions[steps % wrap])
        location = nodes[location][direction]
        steps += 1

    return steps


def simultaneous_travel(directions,nodes):

    steps = [travel(directions, nodes, origin, 'Z') for origin in [n for n in nodes.keys() if n.endswith('A')]]
    
    return lcm(steps)


def main(filepath):

    directions, nodes = parse_input(filepath)

    return travel(directions, nodes), simultaneous_travel(directions, nodes)


print(main('08.txt'))