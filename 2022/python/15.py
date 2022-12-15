#  Very slow. Tried a few tuning techniques, but it has made minimal difference. Judging by comments on the megathread there's just 
#  something about this approach on python that does not allow it to run fast. There might be some lru caching opportunities that
#  would speed things up somewhat, but really this needs a different approach to get the run time down.

class SensorBeacon:

    def __init__(self,*args):

        self.sensor, self.beacon, self.target = args
        self.sensor_y, self.sensor_x = self.sensor
        self.beacon_y, self.beacon_x = self.beacon
        self.manhattan = abs(self.sensor_y-self.beacon_y) + abs(self.sensor_x-self.beacon_x)
        self.sensor_range = (max(0,self.sensor_y - self.manhattan), min(self.target,self.sensor_y + self.manhattan))

    def __str__(self): 
        
        return f"sensor: {self.sensor}, beacon: {self.beacon}, manhattan: {self.manhattan}, sensor_range: {self.sensor_range}"

    def adjust(self,y): return self.manhattan-abs(y-self.sensor_y)


def overlap(a,b): return True if len(range(max(a[0],b[0]),min(a[1],b[1])+1)) > 0 else False


def main(filepath,target=4000000):

    input = list(map(int,''.join([x for x in open(filepath).read().replace(':',',').replace('\n',',') if x in '0123456789-,']).split(',')))
    sensors = [tuple(input[i:i+2][::-1]) for i in range(0,len(input),4)]
    beacons = [tuple(input[i:i+2][::-1]) for i in range(2,len(input),4)]
    results = []

    pairs = [SensorBeacon(*x,target) for x in list(zip(sensors,beacons))]

    for y in (i for i in (range(target//2,target+1), range(target//2+1)) for i in i):

        ranges = [(min(s.sensor_x-s.adjust(y), s.sensor_x+s.adjust(y)), max(s.sensor_x-s.adjust(y), s.sensor_x+s.adjust(y)))
                     for s in pairs if s.sensor_range[0] <= y <= s.sensor_range[1]]

        while len(ranges) > 1:

            if len(ranges) == 2 and not overlap(*ranges[:2]): break

            while not overlap(*ranges[:2]): ranges.append(ranges.pop(0))

            non_overlapping_ranges = []
            start, end = ranges[0]

            for s,e in ranges[1:]:

                if start <= s <= e <= end:      pass
                elif s <= start <= end <= e:    start, end = s,e
                elif s < start and e >= start:  start = s
                elif s <= end and e > end:      end = e
                else:
                    non_overlapping_ranges += [(s,e)]

            ranges = [(start,end)] + non_overlapping_ranges

        if not results: results += [ranges[0][1]-ranges[0][0]+1-len(list(set([s.beacon_x for s in pairs if s.beacon_y == target//2])))]

        if len(ranges) == 2: 
            results += [y + ((min(ranges)[1]+1) * target)]
            break
       
    return tuple(results)
   
print(main('15.txt'))