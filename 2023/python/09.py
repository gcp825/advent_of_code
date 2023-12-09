def next_value(sequence):

    sequences = [] + [sequence]

    while set(sequences[-1]) != {0}:
        sequences += [[y-x for y,x in zip(sequences[-1][1:],sequences[-1])]]

    for i in range(len(sequences)-2,-1,-1):
        sequences[i] += [sequences[i][-1] + sequences[i+1][-1]]

    return sequences[0][-1]


def sum_next_values(sequences):

    return sum([next_value(sequence) for sequence in sequences])


def main(filepath):

    sequences = [list(map(int,x.split(' '))) for x in open(filepath).read().split('\n')]

    return sum_next_values(sequences), sum_next_values([s[::-1] for s in sequences])


print(main('09.txt'))