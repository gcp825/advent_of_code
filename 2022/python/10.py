def main(filepath):

    instructions = open(filepath).read().replace('noop','0').replace('addx ','0\n').split('\n')

    x = 1;  position = 0;  width = 40;  row = '';  display = [];  signal_strength = 0

    for cycle, adjustment in [(i+1,int(y)) for i,y in enumerate(instructions)]:

        if cycle % width == 20: signal_strength += (cycle*x)

        row += chr(0x2588) if abs(position-x) <= 1 else ' '

        if len(row) == width: 
            display += [row]
            row, position = ('',-1)

        position += 1
        x += adjustment

    return '\nPart 1: ' + str(signal_strength) + '\nPart 2:\n\n' + '\n'.join(display) + '\n'

print(main('10.txt'))