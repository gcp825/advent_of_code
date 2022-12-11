#  Pretty happy with this one. Nested list comprehensions can be hard to get your head around, but the gist of what they are doing here is clear
#  and that + the dictionary translations makes for some short, slick code here.

class Cart:

    def __init__(self,*args):

        self.id, self.orientation, self.next_turn, self.track = args
        self.location, self.last_location, self.tick = (self.id, (-1,-1), 0)

        self.adjust_coords    = {'^':(-1,0), '>':(0,1), 'v':(1,0), '<':(0,-1)}
        self.cycle_next_turn  = {'l':'s', 's':'r', 'r':'l'}
        self.apply_turn       = {'^l':'<', '^r':'>', '>l':'^', '>r':'v', 'vl':'>', 'vr':'<', '<l':'v', '<r':'^'}
        self.apply_curve      = {'^`':'<', '^/':'>', '>`':'v', '>/':'^', 'v`':'>', 'v/':'<', '<`':'^', '</':'v'}

    def __str__(self):

        return f"id: {self.id}, tick: {self.tick}, location: {self.location}, orientation: {self.orientation}, next_turn: {self.next_turn}"

    def move(self):

        self.tick += 1
        self.last_location = self.location
        self.location = tuple(map(sum,zip(self.location, self.adjust_coords[self.orientation])))

        if self.track[self.location] == '+':

            self.orientation = self.apply_turn[self.orientation + self.next_turn] if self.next_turn in ('l','r') else self.orientation
            self.next_turn   = self.cycle_next_turn[self.next_turn]

        if self.track[self.location] in ('`','/'):

            self.orientation = self.apply_curve[self.orientation + self.track[self.location]]


def main(filepath):

    input = open(filepath,'r').read().replace('\\','`').split('\n')

    track = dict([((y,x),val.replace('^','|').replace('v','|').replace('<','-').replace('>','-')) for y,row in enumerate(input) 
                                                                                                  for x,val in enumerate(row) if val != ' '])
    carts = [Cart((y,x),val,'l',track) for y,row in enumerate(input) 
                                       for x,val in enumerate(row) if val in ('^','v','<','>')]

    crashed_carts = []

    while len(carts) > 1:

        for cart in carts: cart.move()

        crashed_carts += [cart for i,cart in enumerate(carts) if cart.location in [c.last_location for j,c in enumerate(carts) if j > i]
                                                              or cart.last_location in [c.location for j,c in enumerate(carts) if i > j]
                                                              or cart.location in [c.location for j,c in enumerate(carts) if i != j]]

        carts = [c[1] for c in sorted([(cart.location,cart) for cart in carts if cart.id not in [cc.id for cc in crashed_carts]])]
  

    return crashed_carts[0].location[::-1], carts[0].location[::-1]

                                                              
print(main('13.txt'))