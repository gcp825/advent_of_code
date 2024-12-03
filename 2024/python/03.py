# I have changed: I am no longer allergic to regex. I still don't like it... but it's definitely the easy option here.

from ast import literal_eval
from re import findall

def parse(data, conditionals):

    do, do_not, extension = ("do()", "don't()", "|do\(\)|don't\(\)") if conditionals else (chr(0), chr(0), "")

    matches = "".join(findall("mul\([0-9]{1,3},[0-9]{1,3}\)" + extension, data))
    pairs = [literal_eval(p) for p in "".join([m.split(do_not)[0] for m in matches.split(do)]).split("mul") if p]

    return sum(a*b for a,b in pairs)


def main(filepath):

    data = open(filepath).read()

    return parse(data, False), parse(data, True)

print(main('03.txt'))