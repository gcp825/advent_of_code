def get_code(filepath, method, size=100, code=0):

    dial = size // 2
    rotations = [({'L':-1}.get(line[0],1), int(line[1:])) for line in open(filepath).read().split('\n')]

    for sign, amt in rotations:
        clicks = (amt % size) * sign
        code += (amt // size) * (method-1) + (abs(method-2) if dial == 0 else 0 if 1 <= (dial + clicks) < size else method-1)
        dial = (dial + clicks) % size

    return code


def main(filepath):

    return tuple(get_code(filepath, n) for n in (1,2))

print(main('01.txt'))