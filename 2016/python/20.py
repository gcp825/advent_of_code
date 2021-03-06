#  This was easy... as soon as I tried doing it properly. But I seemed set on cutting corners this morning and as a result spent more time on this than
#  if I'd just started off with a proper frame of mind. Idiot.

def main(filepath):
     
    ranges = sorted([tuple(map(int,x.split('-'))) for x in open(filepath,'r').read().split('\n')])
    consolidated_ranges = []

    for i, r in enumerate(ranges):
        new_low, new_high = r
        check = True

        for low, high in consolidated_ranges:
            if new_low >= low and new_high <= high:
                check = False
                break

        if check:
            for low,high in ranges[:i]+ranges[i+1:]:
                if new_high+1 >= low and new_high < high:
                    new_high = high
            consolidated_ranges += [(new_low,new_high)]

    total_ips = consolidated_ranges[0][0]
    for i,r in enumerate(consolidated_ranges):
        if i > 0:
             total_ips += r[0]-consolidated_ranges[i-1][1]-1
    total_ips += upper_limit-r[1]

    return consolidated_ranges[0][1]+1, total_ips


print(main('20.txt',4294967295))
