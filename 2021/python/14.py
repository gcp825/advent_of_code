#  First we reformat the AB -> C rules input to reflect the two overlapping pairs that will be create by inserting C between A & B e.g. from the example...
#    NN -> C, NC -> B, CB -> H becomes... ('NN',['NC','CN']), ('NC',['NB','BC']), ('CB',['CH','HB'])
#
#  The polymer can also be represented as overlapping pairs, with a count for each e.g. NNCB becomes ('NN',1),('NC',1),('CB',1)
#
#  In each step, we then just translate each pair (and count) to it's corresponding output pairs e.g. ('NN',1),('NC',1),('CB',1) becomes...
#   ('NC',1), ('CN',1) ('NB',1), ('BC',1), ('CH',1), ('HB',1). This format requires minimal storage no matter how many steps we iterate through.
#
#  Finally we just have to reverse engineer the actual number of elements from the final list of overlapping pairs and counts.
#  Let's take ABCCBD stored as ('AB',1), ('BC',1), ('CC',1), ('CB',1), ('BD',1) as our example...
#  
#  For each element, we simply need to sum the counts of any pair containing that element in 1st position, then sum the counts of any pair containing that 
#  element in 2nd position, add those together and then divide the result by 2 to rectify the double counting of elements due to storing overlapping pairs.
#  e.g.
# 
#    A = (1 + 0)//2 = 0 (incorrect)
#    B = (2 + 2)//2 = 2 (correct)
#    C = (2 + 2)//2 = 2 (correct)
#    D = (0 + 1)//2 = 0 (incorrect)
#
#  This gives us correct totals for all but the 'bookend' elements (A & D in this example), which are 1 short due to never overlapping at the ends of the
#  polymer chain. The previous calculation overcorrected these, so we rectify by adding 1 to each of the bookends and we have the correct counts.

from collections import Counter, defaultdict

def parse_file(f):

    polymer, rules = [x for x in open(f,'r').read().split('\n\n')]
    rules = dict([(k,[k[:1]+v, v+k[1:]]) for k,v in [tuple(r.split(' -> ')) for r in [r for r in rules.split('\n')]]])
    pairs = dict(Counter([polymer[i:i+2] for i in range(len(polymer)-1)]))

    return polymer, rules, pairs

def polymerize(pairs,rules,cycles):             

    for _ in range(cycles):

        new_pairs = defaultdict(int)

        for input_pair, input_ct in pairs.items():
            for output_pair, output_ct in [(output_pair,input_ct) for output_pair in rules[input_pair]]:
                new_pairs[output_pair] += output_ct

        pairs = new_pairs

    return pairs

def main(filepath,cycles):

    polymer, rules, pairs = parse_file(filepath)
    pairs = polymerize(pairs,rules,cycles).items()

    distinct_elements = set([k[:1] for k,_ in pairs] + [k[1:] for k,_ in pairs])

    cts = list(sorted( 
             [(sum([v for k,v in pairs if e == k[0]]) + sum([v for k,v in pairs if e == k[1]]) + (1 if e in (polymer[0],polymer[-1]) else 0)) // 2
                 for e in distinct_elements]))

    return cts[-1]-cts[0]

print(main('14.txt',10),main('14.txt',40))