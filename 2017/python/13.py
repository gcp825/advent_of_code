def main(filepath):

    ranges = [(int(x),int(y)-1) for x,y in [tuple(x.split(':')) for x in open(filepath,'r').read().replace(' ','').split('\n')]]
    delay = 0;  caught = True

    severity = sum(depth*(scan_range+1) for depth, scan_range in ranges if depth%(2*scan_range) == 0)

    while caught:
        delay += 1
        for depth, scan_range in ranges:
            caught = True if (delay+depth)%(2*scan_range) == 0 else False
            if caught: break

    return severity, delay

print(main('13.txt'))
