#  Finally... at attempt #3.
#  The recursion wasn't even that bad in the end; I probably had more problems with the key mappings than anything else.

from functools import cache

def map_keys(keypad):

    keys = {key:(y,x) for y,row in enumerate((keypad)) for x,key in enumerate(row)}
    keymap = {}

    for a,b in {(a,b) for a in keys for b in keys if a != '_' and b != '_'}:

        ay, ax, by, bx = (*keys[a], *keys[b])
        moves = [('v' * max(by-ay,0) + '^' * max(ay-by,0)), ('>' * max(bx-ax,0) + '<' * max(ax-bx,0))]
        seqs = [''] if a == b else moves[:1] if ax == bx else moves[1:] if ay == by else [''.join(moves), moves[1]+moves[0]]

        if keys['_'] == (by,ax): seqs.pop(0)
        if keys['_'] == (ay,bx): seqs.pop(1)

        keymap[(a,b)] = tuple(seqs)

    return tuple(keymap.items())


@cache
def count_presses(sequence, keymaps, target_depth, current_depth=0):

    if current_depth < target_depth:

        keymap = dict(keymaps[min(current_depth, 1)])
        presses = 0

        for a, b in zip('A' + sequence, sequence):
            results = []
            for seq in keymap[(a,b)]:
                results += [count_presses(seq + 'A', keymaps, target_depth, current_depth + 1)]
            presses += min(results)

    return len(sequence) if current_depth == target_depth else presses


def process_codes(codes, keymaps, robots):

    return sum(count_presses(code, keymaps, robots) * int(code[:-1]) for code in codes)


def main(filepath):

    codes = open(filepath).read().split('\n')
    keymaps = (map_keys(('789', '456', '123', '_0A')), map_keys(('_^A', '<v>')))

    return tuple(process_codes(codes, keymaps, robots) for robots in (3,26))


print(main('21.txt'))