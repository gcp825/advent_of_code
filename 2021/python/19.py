#  Kept pretty rigidly to the puzzle and just matched the individual scanner cubes to each other and offset their beacon coordinates rather than gradually
#  building up a compound scanner and matching each scanner to that. I figured this approach would actually be quicker, but in practice it's sloooow.
#  More than anything this appears to be due to the initial matching process... perhaps it's doing too much in trying to ensure a definitive match.
#  If I can't figure a way to seriously tune that, I may give the compound mega scanner approach a try and see whether that makes any difference - 
#  if nothing else, it would have saved me the hassle of trying to diagnose why my code wasn't initially working, only to find that two scanner cubes don't
#  seem to have the full 12 match points with another cube (or at least if they do, my matching only seems to find 10, whilst finding 12+ everywhere else).
#  My rotation approach was determined by rotating a Rubik's Cube 24 times such that every orientation was covered (including a return to initial state). 

from itertools import chain

class Scanner:
    
    def __init__(self,id,beacons=[],location=None):

        self.id = id
        self.location = (0,0,0) if location is None else location

        self.orientation = 0;  self.orientations = list('xzzz|yxxx|zyyy|xzzz|yxxx|zyyy'.replace('|',''))

        self.beacons = beacons
        self.update_beacon_distances()
        
    def __str__(self):

        return f"id = {self.id}, size = {self.size}, orientation = {self.orientation}\nlocation = {self.location}\nbeacons = {self.beacons}"

    def new_orientation(self):

        self.orientation = (self.orientation+1)%24
        self.rotate(self.orientations[self.orientation])

    def rotate(self,axis='z'): 

        if   axis.lower() == 'x': self.beacons = [(x,z,-y) for x,y,z in self.beacons]  #  Flip scanner cube up so front face becomes the top face
        elif axis.lower() == 'y': self.beacons = [(z,y,-x) for x,y,z in self.beacons]  #  Swivel scanner cube clockwise on its base (front face --> left face)
        else:                     self.beacons = [(-y,x,z) for x,y,z in self.beacons]  #  Turn front face clockwise (top face --> right face)

        self.update_beacon_distances()

    def update_beacon_distances(self):

        self.distances = [((x,y,z),(xx,yy,zz),(abs(xx-x),abs(yy-y),abs(zz-z))) for x,y,z,xx,yy,zz in
                             [tuple(chain(*[a,b])) for i,a in enumerate(self.beacons) for j,b in enumerate(self.beacons) if i != j]]


def get_potential_matches(scanners):

    matches = []

    for i,scanner in enumerate(scanners):
        print('finding overlaps for scanner',i)
        for other_scanner in scanners[i+1:]:
            overlap = get_overlap(scanner,other_scanner)
            if len(overlap) >= 10:
                matches += [(scanner.id,other_scanner.id)]

    return matches + [(b,a) for a,b in matches]


def get_overlap(a,b):

    matches = [(x[0],y[0],sum(x[2])) for x in a.distances 
                                     for y in b.distances if sum(x[2]) == sum(y[2]) and min(x[2]) == min(y[2]) and max(x[2]) == max(y[2])]

    a_vectors, b_vectors =  list(set([x for x,_,_ in matches])), list(set([y for _,y,_ in matches]))                                                                                       

    overlap = [(a,d) for a,b,c in [(a, sum([1 for x,_,_ in matches if x == a]), sum([z for x,_,z in matches if x == a])) for a in a_vectors] 
                     for d,e,f in [(b, sum([1 for _,y,_ in matches if y == b]), sum([z for _,y,z in matches if y == b])) for b in b_vectors]
                     if b == e and c == f]

    return overlap


def check_orientation(overlap):

    a,b = overlap[0];  x,y,z = (b[0]-a[0],b[1]-a[1],b[2]-a[2])

    match_ct = sum([1 for a,b in overlap if b[0]-x == a[0] and b[1]-y == a[1] and b[2]-z == a[2]])

    return True if match_ct >= 10 else False, (x,y,z)


def main(filepath):

    reports = [list(tuple(map(int,x[n].split(','))) for n in range(len(x)))
                                                    for x in [x.split('\n')[1:] for x in open(filepath,'r').read().split('\n\n')]]

    scanners = [Scanner(i,beacons) for i,beacons in enumerate(reports)]

    wholly_processed, reference_scanners = [], [scanners[0].id]

    matches =  get_potential_matches(scanners)

    while len(reference_scanners) > 0:

        ref_id = reference_scanners.pop(0)

        queue = [(scanners[ref_id],scanners[x]) for i,x in matches if ref_id == i and x not in wholly_processed + reference_scanners]

        for reference, other in queue:

            aligned = False

            while not aligned:
                overlap = get_overlap(reference,other)
                aligned, offset = check_orientation(overlap)
                if not aligned:
                    other.new_orientation()
                    if other.orientation == 0: break

            if aligned:
                print('aligned...',other.id,'to',reference.id)

                other.beacons = [(x-offset[0],y-offset[1],z-offset[2]) for x,y,z in other.beacons]
                other.update_beacon_distances()
                other.location = (-offset[0],-offset[1],-offset[2])

                reference_scanners += [other.id]

        wholly_processed += [ref_id]
        

    manhattan = [sum((abs(b[0]-a[0]),abs(b[1]-a[1]),abs(b[2]-a[2]))) for i,a in enumerate([s.location for s in scanners])
                                                                     for j,b in enumerate([s.location for s in scanners]) if i < j]

    return len(list(set(chain(*[x.beacons for x in scanners])))), max(manhattan)
  
print(main('19.txt'))