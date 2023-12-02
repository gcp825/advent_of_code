# Something a bit different: List comprehensions to convert the numbers to words, then all words back to numbers

def main(allow_text, filepath='01.txt'):

    int_to_word = dict(zip(list('0123456789'), ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']))
    word_to_int = dict([x[::-1] for x in int_to_word.items()])

    words = [''.join([int_to_word.get(x, x if allow_text else '') for x in line]) for line in open(filepath).read().split('\n')]
    numbers = [[word_to_int[line[i:i+n]] for i in range(len(line)) for n in range(3,6) if line[i:i+n] in word_to_int] for line in words]

    return sum([int(x[0]+x[-1]) for x in numbers])

print((main(False), main(True)))