# Original version was a simple for loop incrementing counts. Refactored to a generic function using list comprehension.

def main(filepath):

    depths    = [int(x) for x in open(filepath,'r').read().split('\n')]
    increases = lambda x,y: len([d for i,d in enumerate(x[1:]) if len(x[i+1:]) >= y and sum(x[i+1:i+y+1]) > sum(x[i:i+y])])

    return increases(depths,1), increases(depths,3)
  
print(main('01.txt'))