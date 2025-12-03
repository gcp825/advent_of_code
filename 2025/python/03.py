def parse_input(filepath):

    return [[int(x) for x in line] for line in open(filepath).read().split('\n')]


def get_joltage(bank, number_of_batteries):

    joltage, remaining_bank = [], [] + bank

    while number_of_batteries - len(joltage):

        joltage += [max(remaining_bank[:len(remaining_bank) - (number_of_batteries - len(joltage)) + 1])]
        remaining_bank = remaining_bank[remaining_bank.index(joltage[-1])+1:]

    return int(''.join(map(str,joltage)))


def main(filepath):

    return tuple(sum(get_joltage(bank,n) for bank in parse_input(filepath)) for n in (2,12))


print(main('03.txt'))