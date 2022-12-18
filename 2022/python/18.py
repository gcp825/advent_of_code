def find_surface_area(cubes):

    covered_faces = sum([1 for i,x,y,z in cubes for j,a,b,c in cubes if i != j and ((x == a and y == b and (z in (c-1,c+1)))
                                                                                or  (x == a and z == c and (y in (b-1,b+1)))
                                                                                or  (y == b and z == c and (x in (a-1,a+1))))])
    return len(cubes)*6 - covered_faces


def identify_void_cubes(cubes):

    visited = set();  adj = (-1,0,1)

    min_x, max_x = min([x for x,_,_ in cubes]), max([x for x,_,_ in cubes])
    min_y, max_y = min([y for _,y,_ in cubes]), max([y for _,y,_ in cubes])
    min_z, max_z = min([z for _,_,z in cubes]), max([z for _,_,z in cubes])

    not_cubes = [(x,y,z) for x in range(min_x,max_x+1) for y in range(min_y,max_y+1) for z in range(min_z,max_z+1) if (x,y,z) not in cubes]
    queue     = [min(not_cubes)]

    while queue:

        x,y,z = queue.pop(0)
        visited.add((x,y,z))
        queue += [(x,y,z) for x,y,z in [(x+a,y+b,z+c) for a in adj for b in adj for c in adj if abs(a)+abs(b)+abs(c) == 1] if  (x,y,z) in not_cubes 
                                                                                                                           and (x,y,z) not in visited
                                                                                                                           and (x,y,z) not in queue]

    return [(i,*c) for i,c in enumerate(list(set(not_cubes).difference(visited)))]


def main(filepath):

    cubes = [tuple(map(int,x.split(','))) for x in open(filepath).read().split('\n')]
    enumerated_cubes = [(i,*c) for i,c in enumerate(cubes)]

    surface_area = find_surface_area(enumerated_cubes)

    enumerated_void_cubes = identify_void_cubes(cubes)
    void_surface_area = find_surface_area(enumerated_void_cubes)

    return surface_area, surface_area - void_surface_area
    
print(main('18.txt'))