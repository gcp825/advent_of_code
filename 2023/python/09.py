def differences(sequence):

    def diff(sequence): return [sequence[i+1]-sequence[i] for i in range(len(sequence)-1)]

    sequences = [] + [sequence]
    while not (sum(sequences[-1]) == 0 and len(list(set(sequences[-1]))) == 1):
        sequences += [diff(sequences[-1])]

    return sequences[::-1]


def increase_sequence(sequence):

    sequences = differences(sequence)

    for i in range(1,len(sequences)):
        sequences[i] += [sequences[i][-1] + sequences[i-1][-1]]

    return sequences[-1]


def sum_final_values(sequences):

    return sum([sequence[-1] for sequence in sequences])


def main(filepath):

    sequences = [list(map(int,x.split(' '))) for x in open(filepath).read().split('\n')]

    part_1 = [increase_sequence(seq) for seq in sequences]
    part_2 = [increase_sequence(seq) for seq in [s[::-1] for s in sequences]]

    return sum_final_values(part_1), sum_final_values(part_2)


print(main('09.txt'))