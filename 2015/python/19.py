from hashlib import blake2b as b2b
from random import shuffle
from re import sub

def read_file(filepath):
    
    data = open(filepath,'r').read().split('\n')
    repl = []
    for x in data:
        if x.find(' =>') > 0: repl += [tuple(x.split(' => '))]
            
    molecule = sub(r"([A-Z])", r" \1", x).split()

    return molecule, repl

def determine_molecules(molecule,repl):
    
    formulae = {}
    for f,r in repl:
        for i, element in enumerate(molecule):
            if element == f:
                new_molecule = [] + molecule[0:i] + [r] + molecule[i+1:]
                formula = b2b(''.join(new_molecule).encode('utf-8'),digest_size=16).hexdigest()
                formulae[formula] = formulae.get(formula,0) + 1
                    
    return len(formulae.keys())

def determine_steps(molecule,repl):
    
    replacements = repl;  formula = ''.join(molecule);  ct = 0
    shuffle(replacements)
    
    while formula != 'e':
        
        initial_value = formula
        
        for rep in replacements:
            r,f = rep
            if f in formula:
                ct += formula.count(f)
                formula = formula.replace(f,r)
                
        if formula == initial_value:
            shuffle(replacements)                        #  don't break + recurse here: may not find the answer before hit max recursion depth
            formula = ''.join(molecule);  ct = 0         #  just keep looping instead

    return ct
       
def main(filepath):

    molecule, repl = read_file(filepath)
    pt1 = determine_molecules(molecule,repl)
    pt2 = determine_steps(molecule,repl)
    return pt1,pt2
    
print(main('19.txt'))
