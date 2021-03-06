from json import loads

def read_file(filepath):
    
    return loads(open(filepath,'r').read())

def traverse(obj):

    return (sum(map(traverse, obj))          if type(obj) is list else
            sum(map(traverse, obj.values())) if type(obj) is dict and (part == 1 or 'red' not in obj.values()) else
            obj                              if type(obj) in (int,float) else
            0 )
       
def main(filepath):
    
     return traverse(read_file(filepath))

part = 1;  print(main('12.json'))
part = 2;  print(main('12.json'))
