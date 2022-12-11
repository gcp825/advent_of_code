#  Um... so regex is quite powerful then! Obviously the generated match pattern is not visible in the code and so it doesn't look like somebody has vomited 
#  every character on the keyboard into what is below (which is basically what most regex I've seen before have looked like (and the match pattern for rule 0 
#  is NOT pretty!)). But once I knew what I was doing, it really made this pretty straightforward. Fair play to anyone that didn't use regex and managed to
#  do Part 2 in a non-hacky way... but I wish I'd been comfortable enough with regex to do it like this the first time around!

from copy import deepcopy
import re

def read_file(filepath):
    
    with open(filepath,'r') as f:

        rules, msgs = f.read().split('\n\n')
        
#       dictionary of rules to be used as find (key) and replace (value) input to build our regex match patterns        
        rule_dict = dict((x[0],x[1].replace('"','').strip()) for x in [x.split(':') for x in rules.split('\n')])

#       lookup of rule_id to line nbr in rules file; removed from the rules file so we don't need to cater for it in the regex
        rule_locn = dict((int(v),i) for i,v in enumerate([x[0] for x in [x.split(':') for x in rules.split('\n')]]))
        
#       rules file with corresponding rule ids stripped out - this is the base for building our regex pattern matches
        rules = '\n'.join([x[1].replace('"','').strip() for x in [x.split(':') for x in rules.split('\n')]])   
    
    return rules, rule_dict, rule_locn, msgs

       
def build_pattern(rules, rule_dict, rule_locn, cycles, rule_id):
    
    i = 0; prev_rules = ''
    
    while prev_rules != rules and i < cycles:       #  break when no more replacements to make i.e. all patterns built (non recursive rules)
                                                    #  or enough replacements made to ensure pattern validity for the input (recursive rules)
        prev_rules = deepcopy(rules)        
        for k,v in rule_dict.items():               #  replace rule_ids with the detail of those rules to
            rules = find_and_replace(rules,k,v)     #  ultimately build regex a/b permutation patterns
        i += 1
        
    pattern = [x for x in rules.splitlines()][rule_locn[rule_id]].replace(' ','')    #  return the specified pattern to validate against
   
    return pattern


def find_and_replace(rules,k,v):
    
    find = rf'\b{k}\b'                              #  Find the rule_id (rule_dict key) existing as a whole 'word'
    repl = rf'({v})'                                #  Replace with the corresponding rule detail (rule_dict value) within
    rules = re.sub(find,repl,rules)                 #  parentheses (avoids combining values accidentally & ensures ORs operate correctly)
    
    return rules


def match_pattern(msgs,pattern):
    
    match = rf'\b{pattern}\b'                       #  Find the regex pattern existing as a whole 'word' (or complete msg line 
    ct = len(re.findall(match,msgs))                #  in this case) and return the total number of matches found
    
    return ct

                                                    #  Easiest way to find the nbr of cycles needed for your data with recursive rules
def main(filepath,rule_id=0,cycles=10):             #  is to just keep incrementing until the returned match count stays the same 

    rules, rule_dict, rule_locn, msgs = read_file(filepath)
    pattern = build_pattern(rules, rule_dict, rule_locn, cycles, rule_id)
    ct = match_pattern(msgs,pattern)
    
    return ct

print(main('19a.txt'))
print(main('19b.txt'))                              #  Updated input with rules 8 & 11 amended as suggested
