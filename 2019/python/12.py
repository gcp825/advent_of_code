from math import gcd

class Moon:

    def __init__(self,*args):   
        self.id, self.x, self.y, self.z = args
        self.a, self.b, self.c = (0,0,0)

    def update_velocity(self,object):
        self.a = self.a+1 if self.x < object.x else self.a-1 if self.x > object.x else self.a
        self.b = self.b+1 if self.y < object.y else self.b-1 if self.y > object.y else self.b
        self.c = self.c+1 if self.z < object.z else self.c-1 if self.z > object.z else self.c

    def update_position(self):
        self.x = self.x + self.a;  self.y = self.y + self.b;  self.z = self.z + self.c

def lcm(number_list):

    nums = list(sorted(list(set(number_list))))[::-1]
    while len(nums) > 1:   
        nums = [(nums[0]*nums[1])//gcd(nums[0],nums[1])] + nums[2:]    
    return nums[0]      

def apply_orbit(system):

    for moon in system:
        for satellite in system:
            if moon.id != satellite.id:
                moon.update_velocity(satellite)
    for moon in system:
        moon.update_position()
    return system

def main():

    system = [Moon(0,-8,-18,6), Moon(1,-11,-14,4), Moon(2,8,-3,-10), Moon(3,-2,-16,1)]
    x,y,z = set(), set(), set()
    orbits = [0,0,0]
    days, energy = (0,0)

    while min(orbits) == 0:

        a,b,c = str([m.x for m in system]+[m.a for m in system]), str([m.y for m in system]+[m.b for m in system]), str([m.z for m in system]+[m.c for m in system])        

        if orbits[0] == 0 and a in x: orbits[0] = days
        if orbits[1] == 0 and b in y: orbits[1] = days
        if orbits[2] == 0 and c in z: orbits[2] = days

        x.add(a);  y.add(b);  z.add(c)

        days += 1
        system = apply_orbit(system)
        
        if days == 1000:  energy = sum([sum(map(abs,[m.x,m.y,m.z])) * sum(map(abs,[m.a,m.b,m.c])) for m in system])
        
    return energy, lcm(orbits)

print(main())
