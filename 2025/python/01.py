def get_code(filepath, method, size=100, code=0):

    dial = size // 2
    rotations = [({'L':-1}.get(line[0],1), int(line[1:])) for line in open(filepath).read().split('\n')]

    for sign, amt in rotations:

        whole_rotations = amt // size
        clicks = (amt % size) * sign

        passed_zero = 0 if dial == 0 or 1 <= (dial + clicks) < size else 1
        dial = (dial + clicks) % size

        code += whole_rotations + passed_zero if method == 2 else 1 if dial == 0 else 0

    return code


def main(filepath):

    return tuple(get_code(filepath, n) for n in (1,2))

print(main('01.txt'))