#  Advent of Breadth First Searches continues... a rehash of Day 13, which is a rehash of Day 11...

from enhancements import translate_
from copy import deepcopy
from hashlib import md5

class State:
    
    def __init__(self,x,y):

        self.coords = (x,y);  self.x, self.y = x,y;  self.movelist = ''
 
    def __str__(self):
        
        return f"State: (coords = {self.coords}, moves = {self.movelist})"

    def move(self,direction):
        
        if direction == 'U': self.y = self.y-1;  self.coords = (self.x,self.y)
        if direction == 'R': self.x = self.x+1;  self.coords = (self.x,self.y)
        if direction == 'D': self.y = self.y+1;  self.coords = (self.x,self.y)
        if direction == 'L': self.x = self.x-1;  self.coords = (self.x,self.y)
        
        self.movelist += direction


def explore(extended_passcode):

    return [translate_(str(i),'0123','UDLR','') for i,d in enumerate(md5(extended_passcode.encode('utf-8')).hexdigest()[:4]) if d in 'bcdef']


def determine_moves(passcode,state):

    coords = {'U': (state.x,max(state.y-1,0)), 'R': (min(state.x+1,3),state.y), 'D': (state.x,min(state.y+1,3)), 'L': (max(state.x-1,0),state.y)}
    moves  = []
    directions = explore(passcode+state.movelist)

    for d in directions:    
        move = coords[d]
        if move != state.coords:  moves += [(d,move)]
                
    return moves
                

def main(passcode):
    
    state_queue = [] + [(State(0,0),None)]
    solutions = []

    while len(state_queue) > 0:

        state, move_dir = state_queue[0]
        location = deepcopy(state);  state_queue = state_queue[1:]
        
        if move_dir is not None: location.move(move_dir)

        next_moves = determine_moves(passcode,location)
    
        for move_dir, destination in next_moves:
            if destination == (3,3):
                solution = deepcopy(location)
                solution.move(move_dir)
                solutions += [solution.movelist]
            else:
                state_queue += [(location,move_dir)]

    solutions = sorted(solutions,key=len)

    return solutions[0], len(solutions[-1])
    

print(main('dmypynyp'))
