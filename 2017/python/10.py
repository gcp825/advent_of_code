def hasher(lengths,cycles):

    lengths = list(map(ord,list(lengths))) + [17, 31, 73, 47, 23] if cycles > 1 else list(map(int,lengths.split(',')))
    numbers = list(range(256))
    i = 0;  skip = 0  

    for _ in range(cycles):
        for length in lengths:                      
            numbers = numbers[i:] + numbers[:i] 
            numbers = numbers[:length][::-1] + numbers[length:]
            numbers = numbers[i*-1:] + numbers[:i*-1]
            i = (i + length + skip) % len(numbers)
            skip += 1

    knot_hash = ''.join([('0'+hex(eval('^'.join(list(map(str,numbers[i:i+16])))))[2:])[-2:] for i in range(0,256,16)]) 

    return knot_hash if cycles > 1 else numbers[0]*numbers[1]

def main(lengths):

    return hasher(lengths,1), hasher(lengths,64)

print(main('120,93,0,90,5,80,129,74,1,165,204,255,254,2,50,113'))
