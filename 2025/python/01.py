def get_code(filepath, method, size=100, code=0):

    dial = [size // 2]
    rotations = [({'L':-1}.get(line[0],1), int(line[1:])) for line in open(filepath).read().split('\n')]

    for sign, amt in rotations:

        clicks = (amt % size) * sign
        dial = dial[-1:] + [(dial[-1] + clicks) % size]

        if method == 1 and dial[1] == 0:
            code += 1
        elif method == 2:
            code += (amt // size) + (0 if dial[0] == 0 else 0 if 1 <= (dial[0] + clicks) < size else 1)

    return code


def main(filepath):

    return tuple(get_code(filepath, n) for n in (1,2))

print(main('01.txt'))