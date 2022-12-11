def update_state(state,rules):

    state = '....' + state + '....'

    return state[:2] + ''.join([rules.get(state[i:i+5],'.') for i in range(len(state)-4)]) + state[-2:]


def calculate_total(state,adjust): return sum([i+adjust for i,x in enumerate(state) if x == '#'])


def main(filepath):

    notes = open(filepath,'r').read().split('\n')

    initial_state = notes[0][15:]
    rules         = dict([tuple(x.split(' => ')) for x in notes[2:]])

    state, prev_state, offset, generation, pt1 = (initial_state, (0,''), 0, 0, 0)

    while True:
        
        if state.strip('.') == prev_state[1]: break

        if generation == 20:
            pt1 = calculate_total(state,offset)

        prev_state = (state.find('#')+offset, state.strip('.'))
        state      = update_state(state,rules)

        generation += 1
        offset     -= 4

    increment = (state.find('#')+offset) - prev_state[0]
    remaining = 50*(10**9) - generation

    pt2 = calculate_total(state,(increment*remaining)+offset)

    return pt1, pt2

print(main('12.txt'))