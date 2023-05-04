#  Slow, but it gets there eventually - can't immediately think of a swifter way of doing this.

class Grid:

    def __init__(self, scan, water_sources): 

        self.rock, self.void = self.process_scan(scan)
        self.flow, self.settled = set(), set()
        self.left, self.right, self.left_cascade, self.right_cascade = (), (), False, False
        self.cascades = [(yy if y < yy else y, x) for y,x in water_sources for yy in [min(self.rock)[0]]]


    def process_scan(self, scan):

        scan = open(scan).read().split('\n')
        scan = [(x[0], int(x[2:x.find(',')]), int(x[x.find(' ')+3:x.find('.')]), int(x[x.find('..')+2:])) for x in scan]

        rock = set([(a if axis == 'y' else n, n if axis == 'y' else a) for axis, a, b, c in scan for n in range(b,c+1)])

        miny, maxy = min(rock)[0], max(rock)[0]+1
        minx, maxx = min([x[::-1] for x in rock])[0]-2, max([x[::-1] for x in rock])[0]+2

        boundary = [(y,minx) for y in range(miny,maxy+1)] + [(y,maxx) for y in range(miny,maxy+1)] + [(maxy,x) for x in range(minx,maxx+1)]
        rock.update(boundary)

        return rock, maxy-1


    def apply_flow(self):

        while self.cascades:

            y,x = self.cascades.pop(0)
            y,x = self.apply_vertical_flow(y,x)

            if y < self.void and (y+1,x) not in self.flow:

                settled = self.apply_horizontal_flow(y,x)

                if settled:
                    y,x = self.fill_reservoir(y,x)
                    self.apply_horizontal_flow(y,x)

                if self.left_cascade and self.left not in self.cascades:
                    self.cascades.append(self.left)

                if self.right_cascade and self.right not in self.cascades:
                    self.cascades.append(self.right)


    def apply_vertical_flow(self,y,x):

        yy = min([c[0] for c in (self.rock | self.settled) if c[1] == x and c[0] > y])

        vertical_flow = [(n,x) for n in range(y,yy)]

        self.flow.update(vertical_flow)

        return max(vertical_flow)


    def apply_horizontal_flow(self,y,x):

        self.determine_bounds(y,x)

        horizontal_flow = [(y,n) for n in range(self.left[1], self.right[1]+1)]
        self.flow.update(horizontal_flow)

        return False if self.left_cascade or self.right_cascade else True


    def determine_bounds(self,y,x):

        xx = max([c[1] for c in self.rock if c[0] == y and c[1] < x])
        cascade = [(y,n) for n in range(xx+1,x+1) if (y+1,n) not in self.rock and (y+1,n) not in self.settled][-1:]
        
        self.left, self.left_cascade = (cascade[0], True) if cascade else ((y,xx+1), False)

        xx = min([c[1] for c in self.rock if c[0] == y and c[1] > x])
        cascade = [(y,n) for n in range(x,xx) if (y+1,n) not in self.rock and (y+1,n) not in self.settled][:1]

        self.right, self.right_cascade = (cascade[0], True) if cascade else ((y,xx-1), False)


    def fill_reservoir(self,y,x):

        settled_water = [(y,n) for n in range(self.left[1], self.right[1]+1)]

        self.settled.update(settled_water)
        self.flow = self.flow - self.settled

        y = y-1
        self.determine_bounds(y,x)

        if self.left_cascade or self.right_cascade:
            return y,x
        else:
            return self.fill_reservoir(y,x)


def main(filepath,water_sources):

    x = Grid(filepath,water_sources)
    x.apply_flow()

    return len(list(x.flow|x.settled)), len(list(x.settled))

    
print(main('17.txt',[(0,500)]))