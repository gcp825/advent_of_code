#  Slow, but it gets there eventually - can't immediately think of a swifter way of doing this.

class Ground:

    def __init__(self, scan, springs): 

        self.clay, self.void = self.process_scan(scan)
        self.flow, self.settled = set(), set()
        self.left, self.right, self.left_bounded, self.right_bounded = (), (), False, False
        self.crests = [(yy if y < yy else y, x) for y,x in springs for yy in [min(self.clay)[0]]]


    def process_scan(self, scan):

        scan = open(scan).read().split('\n')
        scan = [(x[0], int(x[2:x.find(',')]), int(x[x.find(' ')+3:x.find('.')]), int(x[x.find('..')+2:])) for x in scan]

        clay = set([(a if axis == 'y' else n, n if axis == 'y' else a) for axis, a, b, c in scan for n in range(b,c+1)])

        miny, maxy = min(clay)[0], max(clay)[0]+1
        minx, maxx = min([x[::-1] for x in clay])[0]-2, max([x[::-1] for x in clay])[0]+2

        boundary = [(y,minx) for y in range(miny,maxy+1)] + [(y,maxx) for y in range(miny,maxy+1)] + [(maxy,x) for x in range(minx,maxx+1)]
        clay.update(boundary)

        return clay, maxy-1


    def apply_flow(self):

        while self.crests:

            y,x = self.crests.pop(0)
            y,x = self.apply_vertical_flow(y,x)

            if y < self.void and (y+1,x) not in self.flow:

                settled = self.apply_horizontal_flow(y,x)

                if settled:
                    y,x = self.fill_reservoir(y,x)
                    self.apply_horizontal_flow(y,x)

                if not self.left_bounded and self.left not in self.crests:
                    self.crests.append(self.left)

                if not self.right_bounded and self.right not in self.crests:
                    self.crests.append(self.right)


    def apply_vertical_flow(self,y,x):

        yy = min([c[0] for c in (self.clay | self.settled) if c[1] == x and c[0] > y])

        vertical_flow = [(n,x) for n in range(y,yy)]

        self.flow.update(vertical_flow)

        return max(vertical_flow)


    def apply_horizontal_flow(self,y,x):

        self.determine_bounds(y,x)

        horizontal_flow = [(y,n) for n in range(self.left[1], self.right[1]+1)]
        self.flow.update(horizontal_flow)

        return True if self.left_bounded and self.right_bounded else False


    def determine_bounds(self,y,x):

        xx = max([c[1] for c in self.clay if c[0] == y and c[1] < x])
        escape = [(y,n) for n in range(xx+1,x+1) if (y+1,n) not in self.clay and (y+1,n) not in self.settled][-1:]
        
        self.left, self.left_bounded = (escape[0], False) if escape else ((y,xx+1), True)

        xx = min([c[1] for c in self.clay if c[0] == y and c[1] > x])
        escape = [(y,n) for n in range(x,xx) if (y+1,n) not in self.clay and (y+1,n) not in self.settled][:1]

        self.right, self.right_bounded = (escape[0], False) if escape else ((y,xx-1), True)


    def fill_reservoir(self,y,x):

        settled_layer = [(y,n) for n in range(self.left[1], self.right[1]+1)]

        self.settled.update(settled_layer)
        self.flow = self.flow - self.settled

        y -= 1
        self.determine_bounds(y,x)

        if self.left_bounded and self.right_bounded:
            return self.fill_reservoir(y,x)
        else:
            return y,x


def main(filepath,springs):

    x = Ground(filepath,springs)
    x.apply_flow()

    return len(list(x.flow|x.settled)), len(list(x.settled))

    
print(main('17.txt',[(0,500)]))