from enhancements import replace_                    #  Personal package of enhancements to standard functions (also in this repo)
import os
if os.name == 'nt':                                  #  Ensure colour compatibility for output via Windows terminal
    import colorama                                   
    colorama.init(strip=True,autoreset=True)  

class Screen:
    
    def __init__(self, x, y):  self.x = x;  self.y = y;  self.display = [x*' ']*y

    def __str__(self):  self.render();  return ''

    def render(self):

        bright = '\033[1m';  green = '\033[32m'
        print(bright + green + ((self.x+2)*'-'))
        for x in self.display: print(bright + green + '¦' + x + '¦')
        print(bright + green + ((self.x+2)*'-'))
        print('\nLit Pixels:', ''.join(self.display).count('#'))

    def row_shift(self,r,x): self.display[r] = self.display[r][x*-1:] + self.display[r][:x*-1]
    
    def col_shift(self,c,x): self.display = [row[:c] + self.display[i-x][c] + row[c+1:] for i,row in enumerate(self.display)]
            
    def polarize(self,x,y):
        for row in range(y):
            self.display[row] = '#'*x + self.display[row][x:]


def main(filepath,x,y):

    find = (' by ','x','rotate ','y=',' =');  repl = (' ',' ','')
    instr = [(x,int(y),int(z)) for x,y,z in [tuple(replace_(i,find,repl).split(' ')) for i in open(filepath,'r').read().split('\n')]]
    
    screen = Screen(x,y)

    for i,x,y in instr:
        if i == 'rect':   screen.polarize(x,y)
        if i == 'row':    screen.row_shift(x,y)
        if i == 'column': screen.col_shift(x,y)

    return screen
        
print(main('08.txt',50,6))
