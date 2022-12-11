#  Started off with the split cuboids into upto 6 sub-cuboids approach... and just couldn't see the wood for the trees when that inevitably
#  didn't work first time: couldn't visualise the overlaps, too many x,y,z,<=,>= all over the code... just, ugh. I couldn't see any way forward
#  with that code but to test it to death with lots of really small hand-crafted cuboid examples to try and unpick the problem and that didn't 
#  sound like fun, so instead I thought my way out of the mess, abandoned all my splitting code and started tinkering with the basics of an 
#  idea that had been gnawing away at the back of my mind... which ultimately lead to this sluggish, clunky, sub-optimal, but WORKING solution!
#
#  The basic premise is that for every overlap we create an additional cuboid with the overlap dimensions and associated with a +1 or -1 value
#  that enforces or negates what is already in that space. When we come to sum everything up, that either results in a net zero or a single
#  counted net positive for those dimensions i.e. off or on. It feels like it could be much slicker... probably a class based solution where I
#  could just keep switching the state of a pre-existing cuboid rather than creating endless duplicates... or I could at least add some pruning
#  to this... but right now, I'm just happy it works.

#  The one thing I do really like about this though is the overlap determination using ranges. It's very neat... which obviously means I 
#  found it on stackoverflow, rather than came up with it myself!

from re import findall
from collections import namedtuple

def read_file(filepath,initialise=False):

    instr = [tuple(map(int,findall(r'-?\d+',x))) for x in open(filepath,'r').read().replace('on','1').replace('off','-1').split('\n')]
    init  = [i for i,x in enumerate(instr) if -50 <= min(x[1:]) <= 50 and -50 <= max(x[1:]) <= 50][-1]

    if initialise is True: return [(v, range(x,xx+1), range(y,yy+1), range(z,zz+1)) for v,x,xx,y,yy,z,zz in instr[:init+1]]
    else:                  return [(v, range(x,xx+1), range(y,yy+1), range(z,zz+1)) for v,x,xx,y,yy,z,zz in instr]


def reboot(instr):

    Cuboid = namedtuple('Cuboid','val x y z')

    updated_cuboids = []

    for cuboid in instr:

        this = Cuboid(*cuboid)
        cuboid_updates = []

        for prev in updated_cuboids:

            cuboid_updates += [prev]

            overlap, dimensions = determine_overlap(prev,this)

            if overlap:

                if   prev.val == 1 and this.val == 1:

                    # prev is currently on, so we add a new negation cube for the overlap
                    # so that this area stills counts as just one when we add the whole of this cube at the end 
                    cuboid_updates += [Cuboid(-1,*dimensions)]

                elif prev.val == 1 and this.val == -1:

                    # prev is currently on, so we add a negation cube for the overlap to turn it off 
                    # we don't add the whole of this cube at the end
                    cuboid_updates += [Cuboid(-1,*dimensions)]

                elif prev.val == -1 and this.val == 1:

                    # prev is a negation cube so we add an on cube for the overlap to cancel that out and
                    # allow the addition of the whole on cube at the end to turn the area on
                    cuboid_updates += [Cuboid(1,*dimensions)]

                else:
                   
                    # this is counterintuitive, but because negation cubes cancel out on cubes and those on cubes will also
                    # have new negation cubes calculated for this overlap, we need to add an on cube to restore the
                    # balance and ensure the cubes net out to zero i.e off
                    cuboid_updates += [Cuboid(1,*dimensions)]


        updated_cuboids = [] + cuboid_updates
        if this.val == 1:
            updated_cuboids += [this]

    return sum([len(cuboid.x)*len(cuboid.y)*len(cuboid.z)*cuboid.val for cuboid in updated_cuboids])


def determine_overlap(prev,this):

    x = range(max(prev.x[0],this.x[0]),min(prev.x[-1],this.x[-1])+1)
    y = range(max(prev.y[0],this.y[0]),min(prev.y[-1],this.y[-1])+1)
    z = range(max(prev.z[0],this.z[0]),min(prev.z[-1],this.z[-1])+1)

    return True if min(len(x),len(y),len(z)) > 0 else False, (x,y,z)


def main(filepath):

    initialise_ct = reboot(read_file(filepath,True))
    reboot_ct     = reboot(read_file(filepath))

    return initialise_ct,reboot_ct
         
print(main('22.txt'))