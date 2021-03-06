#  Advent of Code suddenly obsessed by breadth first searches... which makes me very glad I did produce a proper solution for Day 11, because
#  this code is just a simpler, adapted version of that (structurally they are identical).

from copy import deepcopy

class State:
    
    def __init__(self,x,y):

        self.coords = (x,y);  self.x, self.y = x,y;  self.movelist = '';
 
    def __str__(self):
        
        return f"State: (coords = {self.coords}, moves = {self.movelist})"

    def move(self,direction):
        
        if direction == 'N': self.y = self.y-1;  self.coords = (self.x,self.y)
        if direction == 'E': self.x = self.x+1;  self.coords = (self.x,self.y)
        if direction == 'S': self.y = self.y+1;  self.coords = (self.x,self.y)
        if direction == 'W': self.x = self.x-1;  self.coords = (self.x,self.y)
        
        self.movelist += direction


def explore(x,y,salt=1350):
    
    return '.' if bin((x*x) + (3*x) + (2*x*y) + y + (y*y) + salt)[2:].count('1') % 2 == 0 else '#'
    

def determine_moves(state,visited):

    coords = {'N': (state.x,max(state.y-1,0)), 'E': (state.x+1,state.y), 'S': (state.x,state.y+1), 'W': (max(state.x-1,0),state.y)}
    switch = {'N':'S','E':'W','S':'N','W':'E'}
    moves  = []

    for d in list('ESWN'):
        
        move = coords[d]

        if move != state.coords and switch[d] != state.movelist[-1:] and explore(*move) == '.':
 #      if not an invalid move beyond boundary, not going back the way you came and not an invalid move beyond wall
            move_ct = visited.get(move,-1)
            if len(state.movelist)+1 < move_ct or move_ct < 0:     #  if never reached this location before in this few moves
                visited[move] = len(state.movelist)+1              #  update record of visited states and add to valid moves
                moves += [(d,move)]
                
    return moves, visited
                

def main(start,end):
    
    state_queue = [] + [(State(*start),None)]
    visited = {start:0}
    solutions = []

    while len(state_queue) > 0:

        state, move_dir = state_queue[0]
        location = deepcopy(state);  state_queue = state_queue[1:]
        
        if move_dir is not None: location.move(move_dir)

        next_moves, visited = determine_moves(location,visited)
    
        for move_dir, destination in next_moves:
            if destination == end:
                solution = deepcopy(location)
                solution.move(move_dir)
                solutions += [solution.movelist]
            else:
                state_queue += [(location,move_dir)]

    best_solution = sorted(solutions,key=len)[0]

    return len(best_solution), sum(1 for v in visited.values() if v <= 50)
    

print(main(start=(1,1),end=(31,39)))
