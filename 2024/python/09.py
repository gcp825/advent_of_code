#  This is the horrific naive code I used to get the stars, with no optimisations. It is ugly and comically slow
#  - so much so that it's hard to imagine it being any worse! I simply haven't had a chance to improve this today, so
#  this is it for now: the first one this year that is going to get improved, possibly in 2025, when this is over!

def get_candidate(diskmap, space, file_mode):

    if not file_mode:
        return -1
    else:
        candidate = [i for i,(id,b) in [(n,x) for n,x in enumerate(diskmap)][::-1] if id > 0 and b <= space][:1]
        return candidate[0] if candidate else None


def calc_checksum(element, checksum, pos):

    checksum += sum(max(i*x,0) for x,y in [element] for i in range(pos, pos+y))

    return checksum, pos + element[1]


def rearrange(diskmap, file_mode):

    checksum, pos = (0,0)

    while diskmap:
        id, length = diskmap.pop(0)
        if id < 0:
            space = length
            while space and diskmap:
                idx = get_candidate(diskmap, space, file_mode)
                if idx is not None:
                    id, length = diskmap.pop(idx)
                    if id > 0:
                        blocks = min(length,space)
                        checksum, pos = calc_checksum((id, blocks), checksum, pos)
                        if file_mode:
                            diskmap.insert(idx,(-1,length))
                        if not file_mode and length > space:
                            diskmap += [(id, length-space)]
                        space -= blocks
                else:
                    if file_mode:
                        checksum, pos = calc_checksum((-1, space), checksum, pos)
                    space = 0
        else:
            checksum, pos = calc_checksum((id, length), checksum, pos)

    return checksum


def main(filepath):

    diskmap = [(i//2 if i%2 == 0 else -1, int(blocks)) for i,blocks in enumerate(open(filepath).read())]

    return rearrange([]+diskmap, False), rearrange([]+diskmap, True)


print(main('09.txt'))