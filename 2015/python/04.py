from hashlib import md5

def main(salt,zeroes,nbr=0):
    
    md5_hash = ''
    while md5_hash[0:zeroes] != '0'*zeroes:
        nbr += 1
        md5_hash = md5((salt+str(nbr)).encode('utf-8')).hexdigest()        
    return nbr 

print(main('bgvyzdsv',5))  # pt1
print(main('bgvyzdsv',6))  # pt2
