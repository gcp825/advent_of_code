#  More Advent of Maths. Started looking up Greatest Common Divisors and scribbling numbers again for Part 2 until I remembered what happened last
#  time... and decided I'd probably be fine just throwing logic at it. Took a bit of time to work out how to implement what I had in my head 
#  but working through a noddy example in excel (buses 4,3,2,5 at offset 1,2,4) really helped.

#  Part 2 deliberately a bit more verbose than it needs to be in a code sense because I think it adds a bit of clarity and makes it easier to follow
#  (as well as giving me a few extra lines for the commentary)

def read_file(filepath):
    
    with open(filepath,'r') as f:
        i = [i for i in f.read().split('\n')]

    return (int(i[0]),i[1].split(','))


def next_bus(notes):
    
    wait_times = (lambda ts, bus_ids: [(b - (ts % b),b) for b in [int(x) for x in bus_ids if x.isnumeric()]]) (notes[0],notes[1])
    target_bus = min(wait_times)
    
    return (target_bus[1], target_bus[0])


def next_convoy(notes):
    
    buses = [(i,int(b)) for i,b in enumerate(notes[1]) if b.isnumeric()]
    
    for offset, this_bus_freq in buses:                     #  Iteratively determine when the current bus will arrive at the specified offset against
                                                            #  the ts (that being the start ts all previous buses arrive in a convoy at their correct offsets)
        if offset == 0:
            ts = 0
            convoy_freq = this_bus_freq                     #  The first convoy to compare against is a convoy of one (i.e. the first bus)
                                                            #  The second convoy will be the first bus arriving followed by the 2nd bus at it's correct offset and so on...            
        else:

            while True:
                if (ts + offset) % this_bus_freq == 0:      #  Check if the current bus arrives at the required offset
                    break                                   
                else:                                       #  If not accumulate the ts with the next time the convoy will arrive and check again
                    ts += convoy_freq                      
                                                            #  All buses left at ts 0. Multiplying their frequencies gives the ts they all coincide next. This must also be
            convoy_freq = convoy_freq * this_bus_freq       #  the num of distinct bus location combinations for the convoy (measured in whole ts) until that point in time                           
                                                            #  is reached and the cycle restarts. The offset pattern we're looking for is one of those combinations, so we
    return ts                                               #  simply recalculate convoy frequency when we add a new bus by multiplying current & previous frequency.
      

def main(filepath):
    
    buses = read_file(filepath)
    pt1_bus = next_bus(buses)
    pt2_ts = next_convoy(buses)
    
    return pt1_bus[0]*pt1_bus[1] , pt2_ts


print(main('bus.txt'))
