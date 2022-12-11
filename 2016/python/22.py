#  More BFS. Which is almost the first three initials that came to mind. Another retread of Days 11,13 & 17, this time to break one search up
#  into multiple intermediate steps (i.e an eventual target, and multiple intermediate targets en route).

from enhancements import replace_     #  custom extension of str.replace functionality - see this repo for more details
from copy import deepcopy

class State:
    
    def __init__(self,nodes,first_target,eventual_target):

        self.nodes = dict([((x,y),'_' if used == 0 else '#' if size >= 100 else 'd' if (x,y) == first_target else '.') for x, y, size, used in nodes])
        self.coords = [k for k,v in self.nodes.items() if v == '_'][0]
        self.x, self.y = self.coords

        self.intermediate_target, self.eventual_target = first_target, eventual_target
        x,y = first_target
        self.adjacent_target = (x-1,y) if self.nodes[(x-1,y)] == '.' else (x,y+1) if self.nodes[(x,y+1)] == '.' else (x,y-1) if self.nodes[(x,y-1)] == '.' else (x+1,y)

        self.bounds = {'N':0,'W':0,'E': max([x[0] for x in self.nodes.keys()]),'S': max([x[1] for x in self.nodes.keys()])}
        self.movelist = ''

    def __str__(self):

        self.render()
        return f"State: (coords={self.coords}, eventual_target={self.eventual_target}, adjacent_target={self.adjacent_target}, moves={self.movelist} ({len(self.movelist)}))\n"

    def render(self):

        for row in range(self.bounds['S']+1):
            printline = ''
            for col in range(self.bounds['E']+1):
                if (col,row) == self.adjacent_target and self.nodes[(col,row)] not in ('d','_'):
                    printline += '*'
                else:
                    printline += self.nodes[(col,row)]
            print(printline)
        print(' \n')

    def move(self,direction):

        stash = self.nodes[self.coords]
        
        if direction == 'N': self.y = self.y-1
        if direction == 'E': self.x = self.x+1
        if direction == 'S': self.y = self.y+1
        if direction == 'W': self.x = self.x-1

        self.nodes[self.coords] = self.nodes[(self.x,self.y)]       
        self.coords = (self.x,self.y)
        self.nodes[self.coords] = stash

        self.movelist += direction

    def move_target_data(self):

        x,y = self.intermediate_target
        self.move('N' if self.y-y == 1 else 'E' if x-self.x == 1 else 'S' if y-self.y == 1 else 'W')

        if self.nodes[self.eventual_target] != 'd':
            self.intermediate_target = self.adjacent_target
            x,y = self.adjacent_target
            self.adjacent_target = (x-1,y) if self.nodes[(x-1,y)] == '.' else (x,y+1) if self.nodes[(x,y+1)] == '.' else (x,y-1) if self.nodes[(x,y-1)] == '.' else (x+1,y)


def viable_pairs(nodes):

    viable = []
    for x, y, _ , used in nodes:
        if used:
            for a, b, _ , taken in nodes:
                if (x,y) != (a,b) and (100-taken) >= used:
                    viable += [((x,y),(a,b))]

    return len(viable)


def determine_moves(state,visited):

    coords = {'N': (state.x,max(state.y-1,state.bounds['N'])),  'E': (min(state.x+1,state.bounds['E']),state.y), 
              'S': (state.x,min(state.y+1,state.bounds['S'])),  'W': (max(state.x-1,state.bounds['W']),state.y)}
    switch = {'N':'S','E':'W','S':'N','W':'E'}
    moves  = []

    for d in list('WNES'):
        
        move = coords[d]

        if move != state.coords and switch[d] != state.movelist[-1:] and state.nodes[move] in ('.'):
            move_ct = visited.get(move,-1)
            if len(state.movelist)+1 < move_ct or move_ct < 0:     #  if never reached this location before in this few moves
                visited[move] = len(state.movelist)+1              #  update record of visited states and add to valid moves
                moves += [(d,move)]
                
    return moves, visited
                

def shortest_path(storage):
    
    state_queue = [] + [(storage,None)]
    visited = {storage.coords:0}
    solutions = [];  awaiting_solutions = True

    while len(state_queue) > 0:

        state, move_dir = state_queue[0]
        location = deepcopy(state);  state_queue = state_queue[1:]
        
        if move_dir is not None: location.move(move_dir)

        if awaiting_solutions or len(location.movelist) < min(x[0] for x in solutions):

            next_moves, visited = determine_moves(location, visited)
    
            for move_dir, destination in next_moves:

                if destination == location.adjacent_target:
                    solution = deepcopy(location)
                    solution.move(move_dir)
                    awaiting_solutions = False
                    solutions += [(len(solution.movelist),solution)]
                else:
                    state_queue += [(location,move_dir)]

    best_solution = sorted(solutions)[0][1]

    return best_solution


def main(filepath,data_location=(32,0),destination=(0,0)):

    nodes = [tuple(list(map(int,replace_(x[16:22]+','+x[22:33],[' ','-y','T',' '],['',',']).split(',')))) 
                 for x in open(filepath,'r').read().split('\n') if x.startswith('/dev/grid/node')]

    pt1 = viable_pairs(nodes)

    pt2 = State(nodes,data_location,destination);  data = pt2.nodes[data_location]

    while pt2.nodes[destination] != data:
        pt2 = shortest_path(pt2)         #  moves the empty node into position in the fewest moves
        pt2.move_target_data()           #  moves the target data and sets the new intermediate target position for the empty node
    
    return pt1, len(pt2.movelist)

   
print(main('22.txt'))
