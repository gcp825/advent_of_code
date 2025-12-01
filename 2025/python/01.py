def get_code(filepath, method, dial=50, code=0):

    rotations = [({'L':-1}.get(line[0],1), int(line[1:])) for line in open(filepath).read().split('\n')]

    for sign, amt in rotations:
        code += (amt//100) * (method-1) + (abs(method-2) if dial == 0 else 0 if 1 <= (dial + ((amt%100)*sign)) <= 99 else method-1)
        dial = (dial + ((amt % 100) * sign)) % 100

    return code


def main(filepath):

    return tuple(get_code(filepath, n) for n in (1,2))

print(main('01.txt'))