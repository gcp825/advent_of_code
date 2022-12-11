#  A lot of waffle in the description to disguise the fact that this is kind of a basic read-ahead operation driven by the hashes with 5 repeating characters
#  rather than 3. Use of a set for the keys keeps it simple and prevents any dupes where the hash with a 3-repeat may match to multiple 5-repeat hashes.

from hashlib import md5

def get_hash(salt,n,repeat):

    key = salt+str(n)
    for _ in range(repeat+1):
        key = md5(key.encode('utf-8')).hexdigest()
    return key[::-1]

def main(salt,repeat=0):
    
    n = 0;  limit = 1000;  increment = True;  threes = {};  keys = set()

    while n <= limit:

        key = get_hash(salt,n,repeat)

        for i,x in enumerate(key):
            if key[i:i+3]  == 3*x:
                threes[n] = (key[i:i+3])

            if key[i:i+5]  == 5*x:
                for k in [k for k,v in threes.items() if k+1000 >= n and k < n and v == 3*x]:
                    keys.add(k)

        if n % 1000 == 0 and increment:
            limit += 1000
            threes = dict([(k,v) for k,v in threes.items() if k+1000 >= n])
            if len(keys) >= 64: increment = False
     
        n += 1

    keys = sorted(list(keys))[:64]

    return keys[-1]

print(main('qzyelonm'))
print(main('qzyelonm',2016))
