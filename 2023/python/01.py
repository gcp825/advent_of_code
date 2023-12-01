# Clunky, inefficient starter for 2023!

def insert_numbers(document):

    numbers = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    updated_doc = []

    for item in document:
        line = item
        for i in range(len(line)-1,-1,-1):
            for n, nbr in enumerate(numbers):
                if line[i:i+len(nbr)] == nbr:
                    line = line[:i+len(nbr)] + str(n) + line[i+len(nbr):]
                    break
        updated_doc += [line]
    
    return updated_doc

def main(filepath, part2=False):

    file = open(filepath).read().split('\n')
    document = insert_numbers(file) if part2 else file
    numbers = [[x for x in y if x.isnumeric()] for y in [list(z) for z in document]]

    return sum([int(x[0]+x[-1]) for x in numbers])

print(main('01.txt'), main('01.txt', True))
