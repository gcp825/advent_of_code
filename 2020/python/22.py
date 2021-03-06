from hashlib import blake2b as b2b

def read_file(filepath):
    
    with open(filepath,'r') as f:
        
        data = [x for x in f.read().split('\n\n')]
        player1 = [int(x) for x in data[0].split('\n') if not x.startswith('Player')]
        player2 = [int(x) for x in data[1].split('\n') if not x.startswith('Player')]
        
    return player1, player2


def combat(player1,player2,mode):
    
    if mode == 1:
        player1, player2 = regular_combat(player1,player2)
    else:
        player1, player2 = recursive_combat(player1,player2)
        
    return score(player1,player2)


def regular_combat(player1,player2):
    
    while len(player1) > 0 and len(player2) > 0:
    
        if player1[0] > player2[0]:
            player1, player2 = result(player1,player2)
        else:
            player2, player1 = result(player2,player1)

    return player1, player2


def recursive_combat(player1,player2):
    
    prev_hands = []
    
    while len(player1) > 0 and len(player2) > 0:
        
        prev_hands += [generate_hash(player1,player2)]
        
        if len(prev_hands) > len(list(set(prev_hands))):
            player1 += player2
            player2 = []
        
        elif len(player1)-1 >= player1[0] and len(player2)-1 >= player2[0]:
            player1, player2 = recursive_result(player1,player2)
        
        elif player1[0] > player2[0]:
            player1, player2 = result(player1,player2)
        
        else: player2, player1 = result(player2,player1)
            
    return player1, player2


def result(win,lose): return [] + win[1:] + win[0:1] + lose[0:1], [] + lose[1:]


def recursive_result(player1,player2):
    
    child1 = [] + player1[1:player1[0]+1]
    child2 = [] + player2[1:player2[0]+1]
    
    child1, child2 = recursive_combat(child1,child2)
    
    if len(child1) > len(player1[1:player1[0]+1]):
        player1, player2 = result(player1,player2)
    else:
        player2, player1 = result(player2,player1)
    
    return player1, player2      


def generate_hash(player1,player2):
 
    key = 'p1-' + '|'.join([str(x) for x in player1]) + '-p2-' + '|'.join([str(x) for x in player2])

    return b2b(key.encode('utf-8'),digest_size=16).hexdigest()


def score(x,y):
    
    score = 0;
    z = [] + x if len(x) > 0 else [] + y    
    for i,c in enumerate(z[::-1]): score += c*(i+1)
    
    return 1 if len(x) > 0 else 2, score
    

def main(filepath,mode=1):

    player1, player2 = read_file(filepath)
    winner, score = combat(player1,player2,mode)
    
    return winner, score
        
print(main('22.txt',1))
print(main('22.txt',2))
