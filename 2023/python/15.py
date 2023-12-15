def hash(string, v=0):

    v = ((v + ord(string[0])) * 17) % 256

    return v if len(string) == 1 else hash(string[1:], v)


def hashmap(input):

    instructions = [(a,int(b)) for a,b in [tuple(x.replace('-','=0').split('=')) for x in input]]
    boxes = [{} for _ in range(256)]

    for lens, focal_length in instructions:

        i = hash(lens)

        if focal_length:
            boxes[i][lens] = focal_length

        elif lens in boxes[i]:
            boxes[i].pop(lens)

    return [(i,slot+1,length) for i,b in enumerate(boxes) for slot,length in enumerate(b.values())]


def focusing_power(boxes):

    return sum([(box+1)*slot*length for box, slot, length in boxes])


def main(filepath):

    input  = open(filepath).read().replace('\n','').split(',')
    hashes = [hash(x) for x in input]
    boxes  = hashmap(input)

    return sum(hashes), focusing_power(boxes)


print(main('15.txt'))