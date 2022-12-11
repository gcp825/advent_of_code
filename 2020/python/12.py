
def read_instructions(filepath):
    
    with open(filepath,'r') as f:
        i = [[i[0],int(i[1:])] for i in f.read().split('\n')]
      
    return i   


def rotate_ship(facing,direction,degrees):
     
     d = degrees // 90 if direction == 'R' else (360 - degrees) // 90
     compass = 'NESW'*2
     return compass[compass.find(facing)+d:][0:1]
    

def rotate_waypoint(x,y,direction,degrees):
     
    d = degrees // 90 if direction == 'R' else (360 - degrees) // 90
    i = 0
    
    a,b = x,y
    
    while i < d:
        a,b = b*-1,a
        i += 1
        
    return a,b
  
   
def move(instructions,facing):
     
     f = facing
     x,y = 0,0
    
     for i in instructions:
        
        if i[0] in 'LR':
            f = rotate_ship(f,i[0],i[1])
        else:
            d = f if i[0] in 'F' else i[0]            
            if d in 'N': y -= i[1]
            if d in 'S': y += i[1]
            if d in 'E': x += i[1]
            if d in 'W': x -= i[1]
            
     return abs(x)+abs(y)

    
def relative_move(instructions,waypoint_x, waypoint_y):
     
     x,y = 0,0
     a,b = waypoint_x, waypoint_y
    
     for i in instructions:
      
        if i[0] in 'LR':
            a,b = rotate_waypoint(a,b,i[0],i[1])
            
        elif i[0] in 'F':
            x = x + a*i[1]
            y = y + b*i[1]
            
        else:
            if i[0] in 'N': b -= i[1]
            if i[0] in 'S': b += i[1]
            if i[0] in 'E': a += i[1]
            if i[0] in 'W': a -= i[1]
            
     return abs(x)+abs(y)
  

def main(filepath,facing,waypoint_x,waypoint_y):
 
    i = read_instructions(filepath)
    pt1 = move(i,facing)
    pt2 = relative_move(i,waypoint_x,waypoint_y)
    
    return (pt1,pt2)
    

print(main('instructions.txt','E',10,-1))
