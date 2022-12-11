from intcode import IntcodeComputer    # see intcode.py in this repo

def main(f):

    droid = IntcodeComputer(load=f)
    coords = [(y,x) for y in range(50) for x in range(50)]
    ct = 0

    for y,x in coords:
        result = droid.run([x,y])
        if result == 1:
            ct += 1
        droid.reset(True)

    top_right = 0; x,y = (100,-1)

    while True:

        while top_right == 0:
            y += 1
            top_right = droid.run([x,y])
            droid.reset(True)

        while top_right == 1:
            x += 1
            top_right = droid.run([x,y])
            droid.reset(True)
        x -= 1

        top_left = droid.run([x-99,y]);  droid.reset(True)
        if top_left:
            bottom_left = droid.run([x-99,y+99]);  droid.reset(True)
            if bottom_left:
                bottom_right = droid.run([x,y+99]);  droid.reset(True)
                if bottom_right:
                    break
        top_right = 0

    return ct, ((x-99)*10000) + y
 
print(main('19.txt'))
