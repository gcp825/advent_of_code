#  Literally the same problem as 2020 Day 13, part 2. Here is a better constructed version of that solution. 
#  Originally, I just brute forced every configuration until I found the right one (i.e a different approach to what I did before)...
#  but that ended up being only one line of code less than this, whilst this approach is far more scalable, and instantaneous for the given input.

def main(curr_config, disc_positions):

    time = 0;  i = 0;  cf = 1                    
    target_config = [p-i if 0 < p-i < p else (p+i)%p for i,p in enumerate(disc_positions)]

    while i < len(disc_positions):                      

        if curr_config[i] == target_config[i]:
            cf = cf * disc_positions[i]         #  cf = cumulative frequency of aligned discs so far i.e we get disc 1 in the correct position, then 1,2, then 1,2,3...
            i += 1
        else:
            curr_config = [pos+cf if pos+cf < mx else (pos+cf)%mx for pos,mx in list(zip(curr_config,disc_positions))]
            time += cf

    return time-1                               #  account for 1 second drop time for the capsule to reach the first disc

print(main([11,0,11,0,2,17],[13,5,17,3,7,19]))
print(main([11,0,11,0,2,17,0],[13,5,17,3,7,19,11]))
