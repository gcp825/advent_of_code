#  The somewhat tuned version of the code. It still takes 8 seconds on my pathetic laptop, but that's a significant
#  improvement on what it was. Two distinct loops for the different move/fill space approaches definitely cleaner
#  than one loop full of various if conditions depending on what mode you are running under.

def move_blocks(new_diskmap, diskmap, space, i, moved_files=0):

    while True:

        if i < 0 or space == 0: break

        if diskmap[i][0] < 0:
            i -= 1
        else:
            id, length = diskmap.pop(i)
            if length > space:
                diskmap.insert(i,(id,length-space))
                new_diskmap += [(id,space)]
                space = 0
            else:
                new_diskmap += [(id,length)]
                space -= length
                moved_files += 1
                i -= 1

    return new_diskmap, moved_files, diskmap


def move_files(new_diskmap, diskmap, space, i, moved_files=0):

    while True:

        if i < 0:
            new_diskmap += [(-1,space)]
            space = 0

        if space == 0: break

        if diskmap[i][0] < 0 or diskmap[i][1] > space:
            i -= 1
        else:
            id, length = diskmap.pop(i)
            new_diskmap += [(id,length)]
            diskmap.insert(i,(-1,length))
            space -= length
            moved_files += 1
            i -= 1

    return new_diskmap, moved_files, diskmap


def checksum(diskmap):

    return sum(max(id,0)*i for i,id in enumerate(sum([[x[0]]*x[1] for x in diskmap],[])))


def rearrange(diskmap, move_whole_files):

    diskmap, new_diskmap = [] + diskmap, []
    move = move_files if move_whole_files else move_blocks
    processed, total_files = 0, sum(1 for x in diskmap if x[0] >= 0)

    while processed < total_files:

        id, length = diskmap.pop(0)

        if id >= 0:
            new_diskmap += [(id,length)]
            processed += 1
        else:
            new_diskmap, moved, diskmap = move(new_diskmap, diskmap, length, len(diskmap)-1)
            processed += moved

    return checksum(new_diskmap)


def main(filepath):

    files = [(i//2 if i%2 == 0 else -1, int(length)) for i,length in enumerate(open(filepath).read())]

    return rearrange(files, False), rearrange(files, True)


print(main('09.txt'))