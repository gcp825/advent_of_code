class Monkey:

    def __init__(self,*args):

        self.id, self.items, self.reaction, self.test = args[:4];  self.targets = tuple(args[4:6]);  self.reducer = args[6];  self.inspections = 0

    def __str__(self): 
        
        return f"id: {self.id}, items: {self.items}, reaction: {self.reaction}, test: {self.test}, targets: {self.targets}, inspections: {self.inspections}"

    def examine(self): 

        items = []
        for mod_reductions, divisor, old in self.items:
            new = eval(self.reaction) // self.reducer
            if new >= divisor:
                new = new % divisor
                mod_reductions += 1
            items += [(mod_reductions,divisor,new)]

        self.items = items
        self.inspections += len(self.items)

    def target(self):

        return self.targets[min(self.items[0][2] % self.test,1)]

    def throw(self):

        return self.items.pop(0)

    def catch(self,item):

        self.items += [item]


def lcm(numbers):

    ''' Returns the Least Common Multiple from a supplied list of numbers '''

    def gcd(a, b): return a if b == 0 else gcd(b,a % b)

    nums = list(sorted(list(set(numbers))))[::-1]

    while len(nums) > 1:  nums = [(nums[0]*nums[1]) // gcd(nums[0],nums[1])] + nums[2:] 

    return nums[0]


def main(filepath,rounds,reducer=1):

    divisor = lcm([int(x[3][21:]) for x in [x.split('\n') for x in open(filepath).read().split('\n\n')]])

    monkeys = [Monkey(*m) for m in 
                  [(int(a[7:-1]), [(0,divisor,i) for i in list(map(int,b[18:].split(', ')))], c[19:], int(d[21:]), int(e[29:]), int(f[30:]), reducer)
                      for a,b,c,d,e,f in [tuple(x.split('\n')) for x in open(filepath).read().split('\n\n')]]]

    for _ in range(rounds):

        for i in range(len(monkeys)):

            monkeys[i].examine()

            while monkeys[i].items:

                monkeys[monkeys[i].target()].catch(monkeys[i].throw())

    return [a*b for a,b in [list(sorted([m.inspections for m in monkeys]))[-2:]]][0]


print((main('11.txt',20,3),main('11.txt',10000)))