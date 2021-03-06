#  Having been completely nonplussed about the prospects and benefits of actually writing a code solution for this, I found myself oddly motivated today!
#  And if nothing else it was a very good reminder that whenever comparing against a list of stuff (previously seen states in this case), using a set where
#  possible will noticeably speed things up for anything more than a handful of values.

#  Two key assumptions made in this code:
#     1) Previously seen states can be treated as a pattern i.e. 1 Chip & 3 Generators on Floor 0 can be recorded as 'Xxxx' rather than say 'Aabc' specifically
#        and states with a similar pattern e.g 'Bbcd' can then be ignored as an invalid move (because we've already explored this path with a different permutation).
#        Note that I've simplified this for the explanation as the captured state in the code actually covers all 4 floors and the elevator position.
#     2) Because we're investigating individual moves in order of optimality, the first found solution *should* be the shortest (although there may be other solutions
#        with the same number of moves). This holds true for my input.


from itertools import combinations
from copy import deepcopy

class State:
    
    def __init__(self,floors,floor):

        items = ''.join(sorted(''.join(floors)))
        self.translator = ''.maketrans(items,''.join(list(map(lambda x: 'X' if x.isupper() else 'x',items))),'')

        self.floors = [''.join(sorted(x)) for x in floors];  self.floor = floor;  self.movelist = []
        
        self.state = self.get_state()
        self.target_state = self.get_state(['']*(len(self.floors)-1) + [items], len(self.floors)-1)
        
        
    def __str__(self):
        
        p1 = f"State: (floors: {self.floors}, current floor: {self.floor}, state_id: {self.state}, tgt_state_id: {self.target_state})"
        p2 = f"Move List: (count: {len(self.movelist)}, list: {self.movelist})"
        
        return p1 + '\n' + p2
    

    def get_state(self,floors=None,floor=None):
        
        if floors is None or floor is None:
            floors = self.floors;  floor = self.floor
        
        return str(floor) + ':' + ':'.join(floors).translate(self.translator)
    
    
    def validate(self,items,direction):
        
        idx = self.floor - 1 if direction == '<' else self.floor + 1
        
        if 0 <= idx <= len(self.floors)-1:                                                                    # if destination floor exists:
            new_floors = [] + self.floors
            new_floors[self.floor] = new_floors[self.floor].replace(items[0:1],'').replace(items[1:2],'')     #  remove from current floor (virtually)
            new_floors[idx] = ''.join(sorted(new_floors[idx] + items))                                        #  move to next floor (virtually)
        else:
            return None
        
        for floor in new_floors:                                                                              #  Check modelled floors for validity...
            unpaired_chips = True if sum(1 for x in list(floor) if x.isupper() and x.lower() not in floor) > 0 else False
            generators     = True if sum(1 for x in list(floor) if x.islower()) > 0 else False
            if (unpaired_chips and generators):                                                               #  Cannot have unpaired chips if a generator is present:
                return None                                                                                   #  therefore move is invalid
            
        return self.get_state(new_floors,idx)
            

    def move(self,items,direction):

        self.floors[self.floor] = self.floors[self.floor].replace(items[0:1],'').replace(items[1:2],'')       #  remove from current floor

        self.floor = self.floor - 1 if direction == '<' else self.floor + 1                                   
        self.floors[self.floor] = ''.join(sorted(self.floors[self.floor] + items))                            #  move to next floor

        self.state = self.get_state()
        self.movelist += [(items,direction)]
            

def determine_moves(state,previous_states):

    singles = list(state.floors[state.floor])
    pairs = [''.join(x) for x in combinations(singles,2)]
    moves = [];  valid_moves = []
    
    if state.floor < len(state.floors)-1: moves += [(x,'>') for x in pairs]                                   #  moves added/processed downstream in order of optimality
    if state.floor > 0:                   moves += [(x,'<') for x in singles]    
    if state.floor < len(state.floors)-1: moves += [(x,'>') for x in singles]
    if state.floor > 0:                   moves += [(x,'<') for x in pairs]
        
    for move in moves:
        state_id = state.validate(*move)
        if state_id is not None and state_id not in previous_states:
            if state_id == state.target_state:
                valid_moves += [(move,'solved')]
            else:
                valid_moves += [(move,'unsolved')]
                previous_states.add(state_id)

    return valid_moves, previous_states


def main(floors,start_floor,break_on_first=True):
    
    puzzle = State(floors,start_floor)
    state_queue = [] + [(puzzle,None)]
    previous_states = set();  previous_states.add(puzzle.state)
    solutions = []

    while len(state_queue) > 0:

        state, move = state_queue[0]   
        puzzle = deepcopy(state);  state_queue = state_queue[1:]
        
        if move is not None: puzzle.move(*move)

        next_moves, previous_states = determine_moves(puzzle,previous_states)
    
        for move, status in next_moves:
            if status == 'solved':
                solution = deepcopy(puzzle)
                solution.move(*move)
                solutions += [solution.movelist]
            else:
                state_queue += [(puzzle,move)]

        if len(solutions) > 0 and break_on_first: break

    best_solution = sorted(solutions,key=len)[0]
    for move in best_solution: print(move)
    
    return len(best_solution)

        
print('\nMoves:',main(['Aabc','BC','DdEe',''],0))      #  pt1  - use a distinct single Uppercase Letter to represent a chip
print('\nMoves:',main(['XxYyAabc','BC','DdEe',''],0))  #  pt2  - and the Lowercase version of that letter to represent its Generator
