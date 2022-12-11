#  Basic brute force full calculation approach, using lists and ints throughout to avoid string manipulation performance overhead

def main(data,length):

    data = list(map(int,list(data)))
    while len(data) < length:
        data = data + [0] + [1 if x == 0 else 0 for x in data[::-1]]

    checksum = data[:length]
    while len(checksum) % 2 == 0:
        checksum = [1 if checksum[i] == checksum[i+1] else 0 for i in range(0,len(checksum),2)]

    return ''.join(map(str,checksum))

print(main('10010000000110000',272))
print(main('10010000000110000',35651584))
