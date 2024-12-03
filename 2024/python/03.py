# I have changed: I am no longer allergic to regex. I still don't like it... but it's definitely the easy option here.

import re

def parse(data, conditionals):

    execute, ignore = ("do()", "don't()") if conditionals else (chr(0), chr(0))
    alternates = "|do\(\)|don't\(\)" if conditionals else ""

    matches = "".join(re.findall("mul\([0-9]{1,3},[0-9]{1,3}\)" + alternates, data))
    pairs = [p for p in "".join([m.split(ignore)[0] for m in matches.split(execute)]).split("mul") if p]

    return sum(a*b for a,b in [tuple(map(int, x[1:-1].split(','))) for x in pairs])


def main(filepath):

    data = open(filepath).read()

    return parse(data, False), parse(data, True)

print(main('03.txt'))