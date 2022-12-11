from itertools import combinations
from functools import reduce
from operator  import mul as multiply

def identify_entries(items, total, entries):

    for subset in combinations(entries,items):
        if sum(subset) == total:     
            return (subset, reduce(multiply,subset))
    return None

expenses = [1721,979,366,299,675,1456]

print(identify_entries(2,2020,expenses))  # part 1
print(identify_entries(3,2020,expenses))  # part 2
