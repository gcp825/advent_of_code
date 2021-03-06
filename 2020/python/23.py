def setup_circle(start_cups,total_cups):
    
    circle = {}
    start_seq = [int(c) for c in list(str(start_cups))]    
    if total_cups <= len(start_seq): total_cups = len(start_seq)
    
    for i,c in enumerate(start_seq):               #  build the circle
        if i > 0: circle[start_seq[i-1]] = c        
    if len(start_seq) == total_cups:
        circle[c] = start_seq[0]                   #  point the end cup at the start cup to complete the circle
    else:
        circle[c] = len(start_seq)+1               #  add the first unspecified cup to the circle
        circle[total_cups] = start_seq[0]          #  point the end cup at the start cup to complete the circle
                                                   #  the starting circle contains all non-sequential cups + an implied void of sequential cups
    return start_seq[0], circle

    
def move_cups(start_cup,circle,moves):
    
    i = start_cup;  mn = min(circle); mx = max(circle)
    
    for _ in range(moves):

        removed = []; c = i                        #  get the next 4 cups, removing the first 3 from the circle
        for r in range(4):                         #  the 4th cup will be current cup in the next pass
            c = circle.get(c,c+1)
            if r < 3: removed += [c]

        x = mx if i == mn else i-1                 #  determine the destination cup (x)
        while x in removed:
            x = mx if x == mn else x-1
            
        circle[removed[2]] = circle.get(x,x+1)     #  repoint the 3rd removed cup to point at the cup currently following the destination
        circle[x] = removed[0]                     #  repoint the destination to point at the first of the removed cups
        circle[i] = c                              #  repoint current cup to point at the cup immediately after the space vacated by the removed cups
        i = c                                      #  increment the current cup to the next in the new sequence
        
    if len(circle.keys()) == 9:
        x = 1; cup_order = ''
        for _ in range(8):
            x = circle[x]
            cup_order += str(x)
        return cup_order
    else:
        return circle[1] * circle[circle[1]]
        

def main(start_cups,moves=100,total_cups=0):

    start_cup, circle = setup_circle(start_cups,total_cups)
    output = move_cups(start_cup,circle,moves)
      
    return output

print(main(586439172))                    #pt 1
print(main(586439172,10000000,1000000))   #pt 2
