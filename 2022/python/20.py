from collections import deque

def main(filepath,cycles=10,decrypt_key=811589153):

    data   = deque([(i,int(x)*decrypt_key) for i,x in enumerate(open(filepath).read().split('\n'))])
    length = len(data)

    for _ in range(cycles):

        for orig_idx in range(length):

            while data[0][0] != orig_idx:  data.rotate(-1)

            item = data.popleft()

            data.rotate(-item[1])

            data.appendleft(item)

    while data[0][1] != 0:  data.rotate(-1)

    return data[1000 % length][1] + data[2000 % length][1] + data[3000 % length][1]


print((main('20.txt',1,1),main('20.txt')))