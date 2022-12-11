from collections import namedtuple
from itertools import permutations, combinations_with_replacement as combinations

def read_file(filepath):
    
    Ingredient = namedtuple('Ingredient','name capacity durability flavour texture calories')

    return sorted([Ingredient(x[0],int(x[2]),int(x[4]),int(x[6]),int(x[8]),int(x[10]))
                       for x in [x.split(',') for x in [x for x in open(filepath,'r').read().replace(', ',',').replace(':','').replace(' ',',').split('\n')]]])

def score_recipes(ingredients,teaspoons):
    
    quantities = [x for x in combinations(list(range(0,teaspoons+1)),len(ingredients)) if sum(x) == teaspoons]   #  filter to valid combinations rather than permutations
    best_score = (0,0);  best_meal = (0,0)

    for combination in quantities:
        for q in set(permutations(combination)):                                                                 #  expand to permutations once valid combinations established
            capacity = 0;  durability = 0;  flavour = 0;  texture = 0;  calories = 0
            for x in range(len(ingredients)):
                capacity   += ingredients[x].capacity   * q[x]
                durability += ingredients[x].durability * q[x]
                flavour    += ingredients[x].flavour    * q[x]
                texture    += ingredients[x].texture    * q[x]
                calories   += ingredients[x].calories   * q[x]
            score = max(capacity,0) * max(durability,0) * max(flavour,0) * max(texture,0)
        
            best_score = (q,score) if score > best_score[1] else best_score
            best_meal  = (q,score) if calories == 500 and score > best_meal[1] else best_meal

    return best_score, best_meal

def main(filepath,teaspoons=100):

    return score_recipes(read_file(filepath),teaspoons)

print(main('15.txt'))
