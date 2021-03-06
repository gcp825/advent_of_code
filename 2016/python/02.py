#  Kind of fun even though I attempted to second guess part 2 and though I was in the right area I didn't envisage such a ludicrous second keypad!
#  Nevertheless, if feels like the Keypad Class still made it easier to make the required Part2 changes.

class Keypad:

    def __init__(self,x,y,begin,keys_per_row,lo_key=1):
        
        buttons = list('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ');  nbr = lo_key
        
        self.x = x;  self.y = y;  self.buttons = {};  self.kpr = [x]*y if len(keys_per_row) == 0 else list(keys_per_row)

        for y in range(1,self.y+1):
            
            lo = 1 if self.kpr[y-1] == self.x else ((self.x-self.kpr[y-1])//2)+1
            hi = lo + self.kpr[y-1]
            
            for x in range(lo,hi):
                self.buttons[(y,x)] = buttons[nbr]
                nbr += 1
                
        self.pos = [k for k,v in self.buttons.items() if v == str(begin)][0]
        
    def __str__(self):

        layout = [];  i = 0;  k = list(self.buttons.values())
        for length in self.kpr:
            layout += [k[i:i+length]]
            i += length
        return f"layout: {layout}, current_key: {self.current_key()}"

    def move(self,m):
        y,x = self.pos
        if m == 'L' and len(self.buttons.get((y,x-1),'')) > 0: x -= 1
        if m == 'R' and len(self.buttons.get((y,x+1),'')) > 0: x += 1
        if m == 'U' and len(self.buttons.get((y-1,x),'')) > 0: y -= 1
        if m == 'D' and len(self.buttons.get((y+1,x),'')) > 0: y += 1
        self.pos = (y,x)
        
    def current_key(self): return self.buttons[self.pos]
        
def main(filepath,dimensions,begin,keys_per_row=[]):
    
    instructions = [list(x) for x in open(filepath,'r').read().split('\n')]    
    pad = Keypad(*dimensions,begin,keys_per_row)
    code = ''
    for sequence in instructions:
        for move in sequence: pad.move(move)
        code += pad.current_key()
    return code

print(main('02.txt',(3,3),5))                #  pt1
print(main('02.txt',(5,5),5,(1,3,5,3,1)))    #  pt2
