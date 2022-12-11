def main(filepath):

    passphrases = [x.split(' ') for x in open(filepath,'r').read().split('\n')]

    pt1_ct = 0;  pt2_ct = 0
    for p in passphrases:
        if len(p) == len(list(set(p))): 
            pt1_ct += 1
            if len(p) == len(list(set([''.join(list(sorted(word))) for word in p]))): 
                pt2_ct += 1

    return pt1_ct, pt2_ct

print(main('04.txt'))
