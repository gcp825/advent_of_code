#  Not the nightmare I was expecting for Christmas Day!

def get_loop_size(public_key,subject_nbr,nbr=1):

    loop_size = 0
    while nbr != public_key:
        loop_size += 1
        nbr = (nbr*subject_nbr) % 20201227
        
    return loop_size
        
def get_encryption_key(subject_nbr,loop_size,nbr=1):

    for _ in range(loop_size): nbr = (nbr*subject_nbr) % 20201227
        
    return nbr
 
def main(card_pk, door_pk, subject_nbr=7):
    
    return get_encryption_key(door_pk,get_loop_size(card_pk,subject_nbr))

print(main(12090988,240583))
