def generator(n,d,c): 

    x = 2**31-1
    while True:
        while True:     
            n = (n*c)%x
            if n%d == 0: break

        yield bin(n)[2:].zfill(16)[-16:]

def main(x,y,cycles):

    matches = 0;  a = generator(*x,16807);  b = generator(*y,48271)

    for r in range(cycles):
        if next(a) == next(b): matches += 1

    return matches

print(main((289,1),(629,1),40_000_000))
print(main((289,4),(629,8),5_000_000))
