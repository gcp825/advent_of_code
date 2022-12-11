#  So many missteps and screwups...
#  1) Initialise ALL controllers with -1, not just those without a packet generated already
#  2) Controllers can keep generating packets even with post initialisation -1 input, so keep feeding them -1 until exhausted
#  3) Make sure your intcode computer handles no input being provided without erroring (not required before this puzzle)
#  4) And make sure when handling no input, that you're still maintaining pointer state for when input will be provided next

from intcode import IntcodeComputer    # see intcode.py in this repo
from copy import deepcopy

def build_array(f):

    base_image = IntcodeComputer(load=f)  

    network_array = []
    for i in range(50):
        controller = deepcopy(base_image)
        controller.read([i,-1])
        network_array += [controller]
    network_array += ['' for x in range(205)] + [deepcopy(base_image)]

    return network_array

def process_instr(controller):

    output = []
    if len(controller.input) == 0:  controller.read(-1)
    out = controller.run()

    while controller.active:
        output += [out]
        if len(controller.input) == 0:  controller.read(-1)
        out = controller.run()   

    return output

def network_idle(network_array):

    return True if max([len(controller.input) for controller in network_array[:50]]) == 0 else False

def process_packets(network_array):

    while True:

        for i in range(50):

            output = process_instr(network_array[i])

            while len(output) >= 3:
                addr, x, y = tuple(output[:3])
                output = output[3:]
                recipient = network_array[addr]
                recipient.read([x,y])

        if network_idle(network_array):
            sender, recipient = network_array[255], network_array[0]
            recipient.read(sender.input[-2:])
            sender.output += [sender.input[-1]]
            if len(sender.output) >= 2 and sender.output[-2] == sender.output[-1]:  break

    return network_array[255].input[1], network_array[255].output[-1]

def main(f):

    return process_packets(build_array(f))  

print(main('23.txt'))
