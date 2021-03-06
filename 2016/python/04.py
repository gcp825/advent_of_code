from enhancements import sorted_          #  Private package of function enhancements (also in this repo)
from collections  import Counter

def main(filepath):

    az = 'abcdefghijklmnopqrstuvwxyz';   shift = dict([(az[i],az[i:]+az[:i]) for i in range(26)])
    
    rooms = [(x[::-1][:len(x)-x.find('-')-1],
                 int(x[x.find('[')+1:x.find('-')][::-1]),
                     x[::-1][-6:-1]) for x in [x[::-1] for x in open(filepath,'r').read().split('\n')]]
    
    valid_rms  = [(r[0],r[1]) for r in rooms
                              if r[2] == ''.join(x[0] for x in sorted_(list(Counter(r[0].replace('-','')).items()),1,0,order='da')[:5])]

    for rm, n in valid_rms:
        if len(rm) == 24 and rm[9] == rm[16] and rm[9] in '-':
            idx = n % 26
            room = ''.join([shift.get(rm[i],' '*26)[idx] for i in range(24)])
            if room == 'northpole object storage': break

    return sum(r[1] for r in valid_rms), n

print(main('04.txt'))
