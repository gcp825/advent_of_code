#  Finally... at attempt #3.
#  The recursion wasn't even that bad in the end; I probably had more problems with the key mappings than anything else.

from functools import cache

def map_keys(keypad):

    keys = {key:(y,x) for y,row in enumerate((keypad)) for x,key in enumerate(row)}
    keymap = {(a,b):[] for a in keys for b in keys if '_' not in a+b}

    for a, ay, ax, b, by, bx in [(a,*keys[a],b,*keys[b]) for a,b in keymap]:
        queue, length = [(ay, ax, '')], abs(ay-by) + abs(ax-bx)
        while queue:
            y, x, path = queue.pop(0)
            if (y,x) == (by,bx) and len(path) == length:
                keymap[(a,b)] += [path]
            else:
                if len(path) < length and keys['_'] != (y,x):
                    queue += [(ny, nx, path + d) for ny, nx, d in [(y-1,x,'^'), (y+1,x,'v'), (y,x-1,'<'), (y,x+1,'>')]]

    return tuple((k,tuple(v)) for k,v in keymap.items())


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