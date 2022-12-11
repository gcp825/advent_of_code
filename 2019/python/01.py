def main(f):

    masses = [int(x) for x in open(f,'r').read().split('\n')]
    module_fuel, total_fuel = (0,0)
    for i in range(max(masses)//3):
        masses = [x for x in [x//3-2 for x in masses] if x > 0]
        total_fuel += sum(masses)
        if i == 0: module_fuel = total_fuel
        if len(masses) == 0: break

    return module_fuel, total_fuel

print(main('01.txt'))
