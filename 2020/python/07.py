# I hate recursion and regular expressions. Least favourite challenge so far. Settled on using one and not the other!

def read_file(filepath):
    
    with open(filepath,'r') as rules:
        ruleset = rules.read().split('\n')
 
    return ruleset


def prepare_dict(ruleset):
    
    for i, rule in enumerate(ruleset):
        
        r = [x.strip() for x in rule.rstrip('.')
                                    .replace('bags','')
                                    .replace('bag','')
                                    .split('contain')]                                   #  cleanse + split rule into list of parent & child bags
        
        r[1] = [tuple(x.split(' ',1)) for x in [x.strip() for x in r[1].split(' , ')]]   #  create list of tuples (nbr, desc) for child bags
        r[1] = [(0 if x == 'no' else int(x), y) for x,y in r[1]]                         #  convert child bag nbr to integer 
        ruleset[i] = r                                                                   #  replace in situ

    return {k:v for k,v in (ruleset) if v[0][0] != 0}                                    #  convert to dict removing parents with no child bags


def part1(description, rules):
    
    matches = []
    
    for x, y in rules.items():
        for _, desc in y:
            if description == desc:         
                matches += [x]                                #  recursively append parent matches traversing up through rules            
                matches += part1(x,rules)                     #  may contain duplicate matches i.e. children can have the same parents 

    return matches


def part2(description, rules):

    d = rules.get(description,[])
    
    return 1 + sum(ct * part2(desc,rules) for ct,desc in d)   #  recursively sum/multiply traversing down through rules 


def main(description,filepath):

    ruleset = read_file(filepath)
    rules = prepare_dict(ruleset)
    
    pt1 = len(list(set(part1(description,rules))))            #  deduplicate
    pt2 = part2(description,rules)-1                          #  subtract the original bag from the count
    
    return pt1, pt2

print(main('shiny gold','rules.txt'))

