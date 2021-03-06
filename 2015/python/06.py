def read_file(filepath):
    
    with open(filepath,'r') as f:
        
        actions = []        
        for x in f.read().replace('turn ','').replace('through ','').split('\n'):
            tmp = x.split(' ');
            a,b = tmp[1].split(',');  c,d = tmp[2].split(',');
            x = (int(a),int(c));  y = (int(b),int(d))
            actions += [[tmp[0],y,x]]
            
    return actions

def switch_lights(actions,mode):

    display = {}
    for action, rows, lights in actions:        
        for row in range(rows[0],rows[1]+1):
            for light in range(lights[0],lights[1]+1):
                x = (row,light)
                if mode == 1:
                    display[x] = 1 if action == 'on' else 0 if action == 'off' else (display.get(x,0)+1) % 2
                else:
                    i = 1 if action == 'on' else -1 if action == 'off' else 2
                    display[x] = max(0,display.get(x,0)+i)
                
    return sum(display.values())
          
def main(filepath):
    
     actions = read_file(filepath)
     pt1 = switch_lights(actions,1)
     pt2 = switch_lights(actions,2)
  
     return pt1, pt2
         
print(main('6.txt'))
