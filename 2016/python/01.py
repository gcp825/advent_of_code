#  An object lesson in reading the instructions properly... and how to take some efficient Part 1 code and make it less efficient

class Grid:

    def __init__(self,startpos=(0,0),initial_dir='N'):        
        self.pos = startpos;  self.dir = initial_dir;  self.locations = {(0,0):1};  self.repeat = None
        self.coord = {'N':(0,-1),'E':(1,0),'S':(0,1),'W':(-1,0)};  self.left = {'N':'W','E':'N','S':'E','W':'S'};  self.right = dict((v,k) for k,v in self.left.items())
        
    def __str__(self):
        return f"pos: {self.pos}, dir: {self.dir} \ncoord= {self.coord}, left = {self.left}, right = {self.right} \nfirst repeat: {self.repeat}"

    def move(self,rotate,dist):
        self.dir = self.left[self.dir] if rotate == 'L' else self.right[self.dir]
        coords = self.coord[self.dir]
        for _ in range(dist):
            self.pos = tuple(map(sum,zip(self.pos,coords)))
            ct = self.locations.get(self.pos,0)
            self.locations[self.pos] = ct+1
            if self.repeat is None and ct > 0: self.repeat = self.pos
        
def main(filepath):
    
    city = Grid();  directions = [(x[0:1],int(x[1:])) for x in open(filepath,'r').read().split(', ')]    
    for d in directions: city.move(*d)
    return sum(abs(x) for x in city.pos), sum(abs(x) for x in city.repeat)

print(main('01.txt'))
