# Looks tidier than it was, but still...
# Uses the a-g notation from the puzzle to refer to specific led positions, and works out the equivalent mappings for each input record (e.g. a = b, b = g etc.)
# The mapping is then used to translate the garbled display back to it's intended value, from which we can then identify the digits.

from collections import Counter

def mapper(signals):  
    
    led_ct    = lambda leds, ct: set([k for k,v in Counter(list(''.join([x for x in signals if len(x) == leds]))).items() if v == ct])
    diff      = lambda x,y: min(x - y)
    intersect = lambda x,y: min(x & y)

    one, seven, four, eight = tuple([y for x,y in sorted([(len(x),set(list(x))) for x in signals if len(x) in (2,3,4,7)])])
    leds_in_all_of_235 = led_ct(5,3)
    leds_in_all_of_069 = led_ct(6,3) 
    leds_in_two_of_069 = led_ct(6,2)

    a = diff(seven,one)                                         # intended to actual mappings
    c = intersect(one,leds_in_two_of_069)
    d = intersect(four,leds_in_all_of_235)
    f = intersect(one,leds_in_all_of_069)
    b = diff(four,set([c,d,f]))
    g = diff(leds_in_all_of_235,set([a,d]))
    e = diff(eight,set([a,b,c,d,f,g]))

    return {a:'a', b:'b', c:'c', d:'d',e:'e', f:'f', g:'g'}     # switched to actual to intended for subsequent translation

def main(filepath):

    input    = [(x[:10],x[10:]) for x in [[y for y in x.split()] for x in open(filepath,'r').read().replace('|','').split('\n')]]
    actuals  = ['abcefg','cf','acdeg','acdfg','bcdf','abdfg','abdefg','acf','abcdefg','abcdfg']
    display_total = 0

    for signals, display in input:

        mapping = mapper(signals)
        translation = [str(actuals.index(''.join(sorted([mapping[p] for p in list(digits)])))) for digits in display]
        display_total += int(''.join(translation))
    
    return sum([len([x for x in display if len(x) in [2,3,4,7]]) for _, display in input]), display_total

print(main('08.txt'))