# Brain not functioning at 6.30am this morning:
# Did Part 1 without regex, as always try and avoid using it unless really necessary.
# Then threw Part 1 away and wrote a regex solution for Part 1 & 2... and realised much later there was no need to do that.
# So after another u-turn, here is a nice simple solution for both parts with no regex...

def calculate(text):

    total = 0
    for i in range(len(text)+1):
        if text[i:i+4] == "mul(":
            contents = text[i+4:].split(")")[0]
            if 3 <= len(contents) <= 7:
                left, right = tuple(contents.split(",") + [""])[:2]
                if len(left) <= 3 and len(right) <= 3 and left.isdigit() and right.isdigit():
                    total += int(left)*int(right)
    return total

def main(filepath):

    data = [line.split("don't()") for line in open(filepath).read().split("do()")]
    keep = calculate("".join(x[0] for x in data))
    lose = calculate("".join("".join(x[1:]) for x in data))

    return keep+lose, keep

print(main('03.txt'))