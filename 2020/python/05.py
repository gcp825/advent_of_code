def get_seat(binary_id):
    
    row = int(binary_id[:7].replace('F','0').replace('B','1'),2)
    seat = int(binary_id[7:].replace('L','0').replace('R','1'),2)
    
    return (row * 8) + seat

def process_seats(filepath):
    
    s = []
    
    with open(filepath,'r') as seats:
    
        for line in seats: s = s + [get_seat(line.replace('\n',''))]
        
    return (max(s), sum(range(min(s),max(s)+1)) - sum(s))   
 

print(process_seats('seats.txt'))  # parts 1 & 2
