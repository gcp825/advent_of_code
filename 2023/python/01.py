# Clunky, inefficient starter for 2023. But more sensible than the braindead first attempt that got me the stars!

def extract_number(line, allow_text=False):

    numbers = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'] + list('0123456789')
    extracted = []

    for i in range(len(line)):
        for number, search_string in enumerate(numbers):
            if line[i:].startswith(search_string):
                if search_string.isnumeric() or allow_text:
                    extracted += [str(number%10)]
                break
    
    return int(extracted[0]+extracted[-1])

def main(filepath):

    file = open(filepath).read().split('\n')

    return sum([extract_number(x) for x in file]), sum([extract_number(x, True) for x in file])

print(main('01.txt'))