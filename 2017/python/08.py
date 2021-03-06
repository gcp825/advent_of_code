def main(filepath):

    instr = [tuple(x[0].split(' ')+[x[1][:x[1].find(' ')]]+[x[1][x[1].find(' ')+1:]]) for x in [x.split(' if ') for x in open(filepath,'r').read().split('\n')]]
    registers = {};  high = 0

    for reg, action, amt, register, cond in instr:
        compare = registers.get(register,0)
        update = eval('True if compare ' + cond + ' else False')
        if update:
            current = registers.get(reg,0)
            registers[reg] = current + int(amt) if action == 'inc' else current - int(amt)
        
        high = max(max(list(registers.values())+[0]),high)

    return max(registers.values()), high

print(main('08.txt'))
