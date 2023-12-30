#  For Part 2 used an online Graphviz implementation to visualise the network. In code, have implemented Part 2
#  as two different solutions:
# 
#  2a) Determine the cycle for each circuit by observing the state of the flip-flops upstream of the conjunction
#  2b) Determine the cycle for each circuit by analysing the circuit "diagrammatically" with a mod counter approach

def parse_input(filepath):

    input = [(x[1:] if x[0] in '&%' else x, x[0] if x[0] in '&%' else '?', y.split(',')) 
                for x,y in [z.split('->') for z in open(filepath).read().replace(' ','').split('\n')]]

    downstream = dict([(x,z) for x,_,z in input])

    upstream = {}
    for src, targets in downstream.items():
        for target in targets:
            upstream[target] = upstream.get(target,[]) + [src]

    modtype = dict([(x,y) for x,y,_ in input] + [(x,'?') for x in upstream.keys() if x not in downstream.keys()])
    state   = dict(list(set([(k,0) for k in modtype.keys()] + [(k,0) for k in upstream.keys()])))

    return downstream, upstream, modtype, state


def press_button(modules, criteria, counts=[0,0]):

    p, presses = (0, criteria) if type(criteria) is int else (0, 99**99)
    monitored_modules = criteria if type(criteria) in (list,tuple,set) else []
    early_exit = False

    downstream, upstream, modtype, state = (d.copy() for d in modules)

    while p < presses and not early_exit:

        counts[0] += 1
        queue = [(mod,0) for mod in downstream["broadcaster"]]

        while queue and not early_exit:

            mod, pulse = queue.pop(0)

            if modtype[mod] == "%" and pulse == 1: pass
            else:
                if modtype[mod] == "%" and pulse == 0: 
                    state[mod] = (state[mod]+1)%2
 
                if modtype[mod] == "&":
                    state[mod] = 0 if min([state[src] for src in upstream[mod]]) == 1 else 1
            
                if mod in downstream:
                    queue += [(target,state[mod]) for target in downstream[mod]]

                if monitored_modules:
                    if all([state[mod] for mod in monitored_modules]):
                        early_exit = True

            counts[pulse] += 1
        p += 1
    
    return p if monitored_modules else counts[0]*counts[1]


def lcm(numbers):

    gcd  = lambda a,b: a if b == 0 else gcd(b,a % b)
    nums = list(sorted(list(set(numbers))))[::-1]

    while len(nums) > 1:
        nums = [(nums[0]*nums[1]) // gcd(nums[0],nums[1])] + nums[2:] 

    return nums[0]


def observe_states(modules):

    downstream, upstream, modtype, _ = modules
    queue = ['broadcaster'];  conjunctions = []

    while not conjunctions:
        queue = [m for mod in queue for m in downstream[mod]]
        conjunctions = [m for m in queue if modtype[m] == '&']

    cycles = [press_button(modules,m) for m in [upstream[module] for module in conjunctions]]

    return lcm(cycles) 


def analyse_circuit_diagram(downstream,upstream,modtype,_):

    queue = ['broadcaster'];  conjunctions = [];  cycles = [];  previous = ''

    while not conjunctions:
        queue = [m for mod in queue for m in downstream[mod]]
        conjunctions = [m for m in queue if modtype[m] == '&']

    for module in conjunctions:

        circuit = [m for m in downstream[module] if m in upstream[module]][:1]

        while len(circuit) == 1 or circuit[-1] != previous:

            previous = circuit[-1]
            next_modules = downstream[previous]

            if len(next_modules) > 1:
                circuit += [m for m in next_modules if m != module]
            elif next_modules[0] != module:
                circuit += next_modules
            else: break

        circuit = circuit[::-1]
        bin_cycle = ''.join(['0' if len([m for m in upstream[mod] if m != 'broadcaster']) == 2 else '1' for mod in circuit])

        cycles += [int(bin_cycle,2)]

    return lcm(cycles)


def main(filepath):

    modules = parse_input(filepath)
    part_1  = press_button(modules,1000)
    part_2a = observe_states(modules)
    part_2b = analyse_circuit_diagram(*modules)

    assert part_2a == part_2b

    return part_1, part_2a


print(main('20.txt'))
