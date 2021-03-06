def read_file(filepath):
    
    with open(filepath,'r') as f:
        
        data = [x.replace('(','').replace(')','').split(' contains ') for x in [x for x in f.read().split('\n')]]
        foods = [x[0].split(' ') for x in data]
        allergens = [x[1].split(', ') for x in data]
        
    return foods, allergens

def determine_allergens(foods,allergens):
    
    known_allergens = {}
    distinct_allergens = sorted((list(set([allergen for food in allergens for allergen in food]))))
    
    while len(known_allergens.keys()) < len(distinct_allergens):
    
        for allergen in distinct_allergens:
            if allergen not in known_allergens:
                relevant_foods      = [b for a,b in enumerate(foods) if allergen in allergens[a]]
                theoretical_matches = list(set(relevant_foods[0]).intersection(*relevant_foods))
                possible_matches    = [x for x in theoretical_matches if x not in known_allergens.values()]
                if len(possible_matches) == 1:
                    known_allergens[allergen] = possible_matches[0]
            
    inert_ingredient_ct = len([x for x in [i for f in foods for i in f] if x not in known_allergens.values()])
    dangerous_list = ','.join(x[1] for x in sorted(known_allergens.items()))
    
    return inert_ingredient_ct, dangerous_list

def main(filepath):

    foods, allergens = read_file(filepath)
    pt1, pt2 = determine_allergens(foods,allergens)
    
    return pt1, pt2
        
print(main('21.txt'))
