#  Probably not the most intuitive, understandable code I'll ever write!
#  The boxes dictionary/map is a form of linked list where a single coordinate forming part of a box is associated
#  with a list containing all of the coordinates for that same box.
#  Also the solution *should* work for any size of box/expansion you want to throw at it (within reason) - though
#  I haven't actually tested that!

def parse_input(filepath, box_width):

    raw_grid, moves = [(expand_grid(g, box_width), m) for g,m in [tuple(open(filepath).read().split('\n\n'))]][0]
    grid = [((y,x),col) for y,row in enumerate(raw_grid.split('\n')) for x,col in enumerate(row)]

    box_positions = [tuple([(y,ax) for ax in range(x, x+box_width)]) for (y,x),c in grid if c =='O']
    boxes = dict((location, box) for box in box_positions for location in box)

    wall = {a for a,b in grid if b =='#'}
    location = [a for a,b in grid if b =='@'][0]
    moves = [{'^':(-1,0), '>':(0,1), 'v':(1,0), '<':(0,-1)}[m] for m in ''.join(moves.split('\n'))]

    return wall, boxes, location, moves


def expand_grid(raw_grid, n):

    for char, new_char in zip(('#','O','.','@'), ('#','0','.','.')):
        raw_grid = raw_grid.replace(char, char + (new_char * (n-1)))

    return raw_grid


def get_moveable_boxes(boxes, wall, location, y, x):

    moves = []
    locations = [location]

    while locations:

        current_box_position = boxes[locations.pop(0)]
        new_box_position = tuple([(cy+y, cx+x) for cy,cx in current_box_position])

        if sum(1 for loc in new_box_position if loc in wall) > 0: return []
        else:
            moves += [(current_box_position, new_box_position)]
            adjacent_boxes = list({boxes[loc] for loc in new_box_position if loc in boxes and loc not in current_box_position})
            if adjacent_boxes:
                if y == 0:
                    locations += [adjacent_boxes[0][min(x,0)]]
                else:
                    if len(adjacent_boxes) == 1 and new_box_position == adjacent_boxes[0]:
                        locations += [new_box_position[0]]
                    else:
                        locations += [location for location in new_box_position if location in boxes]

    return list(set(moves))


def move_boxes(boxes, moveable_boxes):

    delete, add = tuple((zip(*moveable_boxes)))

    for box in delete:
        for location in box:
            boxes.pop(location)

    boxes.update((location, box) for box in add for location in box)

    return boxes


def simulate(wall, boxes, location, moves):

    for y,x in moves:
        new_location = (location[0]+y, location[1]+x)
        if new_location not in wall:
            if new_location not in boxes:
                location = new_location
            else:
                moveable_boxes = get_moveable_boxes(boxes, wall, new_location, y, x)
                if moveable_boxes:
                    boxes = move_boxes(boxes, moveable_boxes)
                    location = new_location

    return sum(y*100+x for y,x in [b[0] for b in list(set(boxes.values()))])


def main(filepath):

    return tuple(simulate(*parse_input(filepath, i)) for i in (1,2))


print(main('15.txt'))