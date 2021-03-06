from collections import Counter

def main(filepath):

    particles = [list(map(int,x)) for x in [x.translate(x.maketrans('','','pva=<> ')).split(',') for x in open(filepath,'r').read().split('\n')]]
    particle_ct = len(particles);  prev_ct = 0;  static_ct = 0

    slowest = min((sum(list(map(abs,x[-3:]))),i) for i,x in enumerate(particles))[1]

    while static_ct < 50:

        particles = [[p[0]+p[3]+p[6], p[1]+p[4]+p[7], p[2]+p[5]+p[8], p[3]+p[6], p[4]+p[7], p[5]+p[8], p[6], p[7], p[8]] for p in particles]

        positions = [tuple(x[:3]) for x in particles]
        clashes   = [pos for pos,ct in Counter(positions).items() if ct > 1]

        for i in list(sorted([i for i,x in enumerate(positions) if x in clashes]))[::-1]:  particles.pop(i)

        prev_ct, particle_ct = particle_ct, len(particles)

        static_ct = static_ct + 1 if prev_ct == particle_ct else 0 

    return slowest, len(particles)

print(main('20.txt'))
