from itertools import permutations

def read_file(filepath):
    
    data = [x.split('|') for x in open(filepath,'r').read().replace(' to ','|').replace(' = ','|').split('\n')]
    legs   = dict([((x[0],x[1]),int(x[2])) for x in data] + [((x[1],x[0]),int(x[2])) for x in data])
    places = list(set([k[0] for k in legs.keys()]))
    routes = list(set([min(x,x[::-1]) for x in list(permutations(places,len(places)))]))

    return (routes, legs)

def analyse_routes(routes,legs):

    longest_distance = 0;  shortest_distance = sum(legs.values())
    
    for r in routes:
        distance = 0
        for i, dest in enumerate(r[1:]): distance += legs[(r[i],dest)]
        shortest_distance = min(distance,shortest_distance)
        longest_distance  = max(distance,longest_distance)
  
    return (shortest_distance, longest_distance)

def main(filepath):
    
    routes, legs = read_file(filepath)
    return analyse_routes(routes,legs)

print(main('9.txt'))
