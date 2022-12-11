def main(filepath):

    file = open(filepath,'r').read()
    i, score, total = (0,0,0);  start = None;  trash = ''

    while True:
        if   file[i:i+1] == '':                     break
        elif file[i:i+1] == '!':                    i += 1
        elif file[i:i+1] == '<' and start is None:  start = i
        elif file[i:i+1] == '>':                     
            trash += file[start+1:i]
            file   = file[:start] + file[i+1:]
            i = start-1  
            start = None
        i += 1

    file = list(filter(lambda x: True if x in '{}' else False,file))

    for x in file:
        if x == '{':  score += 1;  total += score
        if x == '}':  score -= 1

    i = 0;  non_cancelled = len(trash)
    while i < len(trash):
        if trash[i] == '!': i += 1;  non_cancelled -= 2
        i += 1

    return total, non_cancelled

print(main('09.txt'))
