def main(f,w,h):

    layers = [];  image = [];  i = 0;  chunk = w*h
  
    data = open(f,'r').read().strip('\n')

    while i < len(data):
        layer = []
        temp = data[i:i+chunk]
        for j in range(0,chunk,w):
            layer += [temp[j:j+w]]
        layers += [layer]
        i += chunk

    pt1 = min([(x.count('0'), x.count('1')*x.count('2')) for i,x in enumerate([''.join(x) for x in layers])])[1]

    for row in range(h):
        row_image = ''
        layer = [x[row] for x in layers]
        for i in range(w):
            visible_pixel = (''.join([x[i] for x in layer]).strip('2')+'2')[0]
            row_image += visible_pixel
        image += [row_image.translate(''.maketrans('120','#  ',''))]

    print('Part 1:',pt1,'\n\nPart 2:','\n')
    for row in image: print(row)
    return '\n'

print(main('08.txt',25,6))
