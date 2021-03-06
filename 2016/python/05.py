#  If you're going to pepper the puzzle with references to WarGames at least call it Global Thermonuclear Door! Anyway...
#  This is really slow: Python is not fast at calculating 27m+ hashes, especially on my pathetically weak netbook.
#  First attempted performance improvement: updated to cache the hasher - the reddit megathread suggest this speeds thing up... and it does, but no where near enough!
#  Second performance improvement: tried multiprocessing to split the work over multiple cpus... but this pickles objects and hashlib objects can't be pickled.
#  So tried a threading solution (multiprocessing.dummy replicates the multiprocessing syntax entirely, but uses threading instead) but as I/O isn't really the 
#  problem here (CPU is), it only makes a tiny dent. Nevertheless, I'm keeping this version of the code as a multiprocessing/threading example for future reference.

from itertools import repeat, chain
from hashlib   import md5
import multiprocessing.dummy as multiprocessing

def get_hashes(md5_hasher,ranges):

    hashes = []
    with multiprocessing.Pool(4) as pool:
        hashes += pool.starmap(process_range, zip(repeat(md5_hasher), ranges))
        
    return [v for k,v in sorted(list(chain(*hashes)))]

def process_range(md5_hasher,r):

    hashes = []
    for n in r:
        hasher = md5_hasher.copy()
        hasher.update(str(n).encode('utf-8'))
        val = hasher.hexdigest()
        if val[0:5] == '00000':
            hashes += [(n,val[5:7])]            
    return hashes
        
def main(salt,size=1000000,limit=28):
    
    md5_hasher = md5();
    md5_hasher.update(salt.encode('utf-8'))

    hashes = get_hashes(md5_hasher, [range(x*size,(x*size)+size) for x in range(0,limit)])
    
    pwd1, pwd2 = (''.join([x[0] for x in hashes[0:8]]), 8*'.')

    for x in [x for x in hashes[::-1] if x[0] in '01234567']: pwd2 = pwd2[:int(x[0])] + x[1] + pwd2[int(x[0])+1:]

    return pwd1, pwd2

if __name__ == "__main__": print(main('wtnhxymk'))
