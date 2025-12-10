# Part 1 only, because Part 2 is ugh. Some other time...
# Even this isn't the finished article as I haven't fully minimised the number of possibilities
# being added to the queue (some buttons are being pressed more than once) but the search space
# is so small the inefficiency doesn't matter.

class Machine:

    def __init__(self,pattern,buttons,joltage,on=False,presses=0,state=None):

        self.pattern, self.buttons, self.joltage = pattern, buttons, joltage
        self.on, self.presses = on, presses
        self.state = state if state else tuple([0] * len(self.pattern))

    def __str__(self):

        return f"On: {self.on} State: {self.state} Pattern: {self.pattern} Buttons: {self.buttons}"


    def copy(self):

        return Machine(self.pattern,self.buttons,self.joltage,self.on,self.presses,self.state)


    def push_button(self,button):

        self.state = tuple((light+1) % 2 if i in self.buttons[button] else light for i,light in enumerate(self.state))
        self.on = True if self.state == self.pattern else False
        self.presses += 1


def parse_input(filepath):

    machines = [line.split() for line in open(filepath).read().split('\n')]
    patterns = [tuple(1 if val == '#' else 0 for val in machine[0][1:-1]) for machine in machines]
    buttons  = [tuple(tuple(map(int,val[1:-1].split(','))) for val in machine[1:-1]) for machine in machines]
    joltage  = [list(map(int,machine[-1][1:-1].split(','))) for machine in machines]

    return list(tuple(zip(patterns,buttons,joltage)))


def push_buttons(machine):

    queue = [(machine.copy(),i) for i in range(len(machine.buttons))]
    seen = {machine.state}


    while queue:
        machine, button = queue.pop(0)
        machine.push_button(button)
        if machine.on: break
        if machine.state not in seen:
            seen.add(machine.state)
            queue += [(machine.copy(),i) for i in range(len(machine.buttons)) if i != button]

    return machine.presses


def main(filepath):

    machines = [Machine(*args) for args in parse_input(filepath)]
    presses  = sum(push_buttons(machine) for machine in machines)

    return presses


print(main('10.txt'))
