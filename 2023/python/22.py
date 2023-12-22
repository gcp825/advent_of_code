def parse_input(filepath):

    bricks = [tuple(map(int,x.split(','))) for x in open(filepath).read().replace('~',',').split('\n')]

    return [brick for _, _, brick in sorted([(b[2],b[5],b) for b in bricks])]


def resting_on(cubes, stack):

    below = [(x,y,z-1) for x,y,z in cubes]
    supported = [stack[b] for b in below if b in stack and b not in cubes]

    return sorted(list(set(supported)))


def establish_stack(bricks):

    stack = {};  parent_to_child = {};  child_to_parent = {}

    for id,(sx,sy,sz,ex,ey,ez) in enumerate(bricks):

        cubes = [(x,y,z) for x in range(sx,ex+1) for y in range(sy,ey+1) for z in range(sz,ez+1)]

        while min([c[2] for c in cubes]) > 1:

            supported_by = resting_on(cubes,stack)

            if not supported_by:
                cubes = [(x,y,z-1) for x,y,z in cubes]
            else:
                child_to_parent[id] = supported_by
                for parent in supported_by:
                    parent_to_child[parent] = parent_to_child.get(parent,[]) + [id]
                break

        stack.update([(c,id) for c in cubes])

    return id+1, parent_to_child, child_to_parent


def disintegrate(bricks, parent_to_child, child_to_parent):

    required = len(list(set([p for p,kids in parent_to_child.items() for c in kids if len(child_to_parent[c]) == 1])))

    return bricks - required


def chain_reaction(_, parent_to_child, child_to_parent):

    falling_bricks = 0

    for parent in parent_to_child.keys():
        
        falling = set([parent]);  queue = [parent]

        while queue:
            p = queue.pop(0)
            children = parent_to_child[p]
            for c in children:
                parents = child_to_parent[c]
                if len(parents) == len([p for p in parents if p in falling]):
                    falling.add(c)
                    if c in parent_to_child and c not in queue:
                        queue += [c]

        falling_bricks += len(list(falling)) - 1

    return falling_bricks


def main(filepath):

    bricks = parse_input(filepath)
    stack  = establish_stack(bricks)

    return disintegrate(*stack), chain_reaction(*stack)


print(main('22.txt'))