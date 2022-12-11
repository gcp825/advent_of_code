class World:

    def __init__(self,santas=1,startpos=(0,0)):        
        self.house = [startpos]*santas;  self.houses = {startpos:santas};  self.santas = santas;  self.idx = 0

    def __str__(self):
        return f"santas: {self.santas}, current houses: {self.house}, houses with gifts: {self.houses}"

    def move(self,d):
        direction = (0,-1) if d == '^' else (1,0) if d == '>' else (0,1) if d == 'v' else (-1,0)
        next_house = tuple(map(sum,zip(self.house[self.idx],direction)))
        self.houses[next_house] = (self.houses.get(next_house,0) + 1)
        self.house[self.idx] = next_house
        self.idx = 0 if self.idx + 1 == self.santas else self.idx + 1

def read_file(filepath):
    
    with open(filepath,'r') as f:        
       directions = f.read().split('\n')[0]
    return directions

def deliver_gifts(directions,santas):
    
    world = World(santas)
    for d in directions: world.move(d)   
    return world
       
def main(filepath):
    
    directions = read_file(filepath)
    pt1 = deliver_gifts(directions,1)
    pt2 = deliver_gifts(directions,2)    
    return len(pt1.houses), len(pt2.houses)
        

print(main('3.txt'))

