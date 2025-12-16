#  Spent ages trying to brute force Part 2 with various different methods to try and pick the optimal
#  button to press at each point to minimise the size of the search space. Whilst I was able to calculate
#  the result for a decent number of the machines, there were just some that have been deliberately
#  configured to make the number of combinations waaay too big for this approach. So eventually gave in
#  and went for what I'd been trying to avoid: an unsatisfactory z3 solution with the associated pain of
#  dealing with the z3 "documentation". Even that wasn't straightforward: I spent too long trying to
#  solve with the general Solver class I'd used once before (2023 Day 24) before finding Optimize.

from z3 import Int, Optimize, Sum

class Machine:

    def __init__(self,pattern,buttons,joltage,on=False,presses=0,pressed=(),state=None):

        self.pattern, self.buttons, self.joltage = pattern, buttons, joltage
        self.on, self.presses, self.pressed = on, presses, pressed
        self.state = state if state else tuple([0] * len(self.pattern))

    def __str__(self):

        return f"On: {self.on} State: {self.state} Pattern: {self.pattern} Buttons: {self.buttons}"

    def copy(self):

        return Machine(self.pattern,self.buttons,self.joltage,self.on,self.presses,self.pressed,self.state)

    def push_button(self,button):

        self.state = tuple((light+1) % 2 if i in self.buttons[button] else light for i,light in enumerate(self.state))
        self.on = True if self.state == self.pattern else False
        self.presses += 1
        self.pressed = (*self.pressed,button)


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
            queue += [(machine.copy(),i) for i in range(len(machine.buttons)) if i not in machine.pressed]

    return machine.presses


def z3_solve(machine):

    variables   = [Int(f'v{n}') for n in range(len(machine.buttons))]
    constraints = [v >= 0 for v in variables]
    equations   = [Sum(*(variables[i] for i, button in enumerate(machine.buttons) if counter in button)) == jolts
                                      for counter, jolts in enumerate(machine.joltage)]
    solver = Optimize()
    solver.add(*constraints,*equations)
    solver.minimize(Sum(variables))
    solver.check()

    results = solver.model()

    return sum(int(str(results[variable])) for variable in results)


def main(filepath):

    machines = [Machine(*args) for args in parse_input(filepath)]
    presses  = sum(push_buttons(machine) for machine in machines)

    return presses, sum(z3_solve(machine) for machine in machines)


print(main('10.txt'))