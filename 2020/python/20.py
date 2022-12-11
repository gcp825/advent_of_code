#  Really enjoyed this one (that wouldn't have been the case if I cared about getting stars as quickly as possible!). Arguably went a bit overboard with 
#  some of it - the Tile class was really helpful, but probably didn't need to be subclass of Image. The conversion of edges to binary to signed integers 
#  (e.g. '.##..#.#..' = 0110010100 = 404, with -404 representing the inverse of that ('..#.#..##.'))  worked really well for easily determining potentially 
#  matching tiles and being able to visually verify that. Plus it's my best performing AoC solution in terms of what it's doing versus speed of result -
#  without even trying!

import re
import os
if os.name == 'nt':                                  #  Ensure colour compatibility for output via Windows terminal
    import colorama                                   
    colorama.init(strip=True,autoreset=True)  

class Image:
    
    def __init__(self, nbr, detail, len_x, len_y):

        self.nbr = nbr;  self.detail = detail;  self.len_x = len_x;  self.len_y = len_y
        self.image_id = int(''.join(self.detail),2)

    def __str__(self):
        
        p_image_id = self.image_id if len(str(self.image_id)) <= 33 else str(self.image_id)[:16] + '\u2026' + str(self.image_id)[-16:]
        return f"nbr = {self.nbr}, len_x = {self.len_x}, len_y = {self.len_y}, image_id = {p_image_id}"

    def render(self,chars='.#@'):

        bright = '\033[1m';  blue = '\033[34m';  green = '\033[32m'
        
        for i in self.detail:
            p = bright + blue + i.replace('0',chars[0]).replace('1',chars[1]).replace('2',green + chars[2] + blue)     #  Set bright + blue as standard colour then set
            print(p)                                                                                                   #  monsters green, resetting to blue after each char

    def rotate(self,clockwise=True,display=False):

        new_detail = []
        for i in range(self.len_x):            
            if clockwise: new_detail += [''.join([line[i] for line in self.detail][::-1])]
            else:         new_detail += [''.join([line[::-1][i] for line in self.detail])]

        self.detail = new_detail
        self.image_id = int(''.join(self.detail),2)
        self.len_x, self.len_y = self.len_y, self.len_x
        if display: self.render()
        
    def flip_x(self,display=False): 

        self.detail = self.detail[::-1]
        self.image_id = int(''.join(self.detail),2)
        if display: self.render()

    def flip_y(self,display=False): 

        self.detail = [line[::-1] for line in self.detail]
        self.image_id = int(''.join(self.detail),2)
        if display: self.render()
        
    def remove_edges(self,display=False):

        self.detail = [line[1:-1] for i,line in enumerate(self.detail) if i not in (0,self.len_y-1)]
        self.image_id = int(''.join(self.detail),2)
        self.len_x -= 2;  self.len_y -= 2;
        if display: self.render()

class Tile(Image):

    def __init__(self, nbr, detail, len_x, len_y, edges):

        self.left, self.top, self.right, self.bottom = edges
        self.style = 'unknown';  self.outer_edges = tuple()
        super().__init__(nbr, detail, len_x, len_y)

    def __str__(self):

        if len(str(self.left) + str(self.top) + str(self.right) + str(self.bottom)) == 0:
            desc = super().__str__()
        else:
            edges = (self.left, self.top, self.right, self.bottom)
            p_image_id = self.image_id if len(str(self.image_id)) <= 33 else str(self.image_id)[:16] + '\u2026' + str(self.image_id)[-16:] 
            desc  = f"nbr = {self.nbr}, style = {self.style}, len_x = {self.len_x}, len_y = {self.len_y}, "
            desc += f"edges = {edges}, outer_edges = {self.outer_edges}, image_id = {p_image_id}"
        return desc

    def rotate(self,clockwise=True,display=False):
        
        if clockwise:
            self.left, self.top, self.right, self.bottom = (self.bottom, self.left*-1, self.top, self.right*-1)
        else:
            self.left, self.top, self.right, self.bottom = (self.top*-1, self.right, self.bottom*-1, self.left)
        super().rotate(clockwise,display)

    def flip_x(self,display=False): 

        self.left, self.top, self.right, self.bottom = (self.left*-1, self.bottom, self.right*-1, self.top)
        super().flip_x(display)

    def flip_y(self,display=False): 

        self.left, self.top, self.right, self.bottom = (self.right, self.top*-1, self.left, self.bottom*-1)
        super().flip_y(display)
        
    def remove_edges(self,display=False):

        self.left = self.top = self.right = self.bottom = '';  self.outer_edges = tuple()
        super().remove_edges(display)


def build_lookup(x):

    lines = {}
    for i in range(int('1'*x,2)+1):
        
        a = bin(i)[2:].rjust(x,'0')
        b = a[::-1]
        
        if a == b:  lines[i] = a; lines[i*-1] = b
        elif a < b: lines[i] = a
        else:       lines[int(b,2)*-1] = a
        
    lookup = dict([(v,k) for k,v in sorted(lines.items())])
    
    return lookup


def initialise_tiles(filepath,lookup,x,y):
    
    with open(filepath,'r') as f:
        
        data = [t for t in f.read().replace('.','0').replace('#','1').split('\n\n')]
        tiles = []
        
        for tile in data:
            
            header, *detail = tile.split('\n')            
            top = detail[0];  bottom = detail[y-1];  left = ''.join([i[0] for i in detail]);  right = ''.join([i[y-1] for i in detail]); 
            
            tiles += [Tile(int(header[:-1].split(' ')[1]), detail, x, y, (lookup[left],lookup[top],lookup[right],lookup[bottom]))]

    return tiles


def categorise_tiles(tiles):
                     
    for tile in tiles:
        
        edges = set([abs(x) for x in [tile.left, tile.top, tile.right, tile.bottom]])
        
        all_other_edges = set([abs(x) for x in [t.left for t in tiles if t.nbr != tile.nbr]  +
                                               [t.top for t in tiles if t.nbr != tile.nbr] +
                                               [t.right for t in tiles if t.nbr != tile.nbr] +
                                               [t.bottom for t in tiles if t.nbr != tile.nbr]])

        unmatched = [x for x in edges if abs(x) not in edges.intersection(all_other_edges)]
        
        tile.style = 'regular' if len(unmatched) == 0 else 'edge' if len(unmatched) == 1 else 'corner'
        tile.outer_edges = tuple(unmatched)

    return tiles


def determine_layout(tiles):
                     
    layout = {};  x = 0;  y = 0;  max_x = len(tiles); max_y = len(tiles)
    
    regular = [t for t in tiles if t.style == 'regular']
    edges =   [t for t in tiles if t.style == 'edge']
    corners = [t for t in tiles if t.style == 'corner']
    
    while len(layout) < len(tiles):
        
        if x+y == 0:                                                                           #  very first corner tile
            tile = corners[0]
            if abs(tile.bottom) in tile.outer_edges: tile.flip_x()
            if abs(tile.right)  in tile.outer_edges: tile.flip_y()
            
        elif y == 0:                                                                           #  top row, any tile but first
            tile = select_tile(layout[(x-1,y)].right,None,edges,corners)
#           set row length once row 0 complete
            if tile.style == 'corner': max_x = x
            
        elif x == 0:                                                                           #  first tile of any other row
            tile = select_tile(None,layout[(x,y-1)].bottom,edges,corners)
        
        elif 0 < y < max_y:                                                                    #  middle row(s), any tile but first
            tile = select_tile(layout[(x-1,y)].right, layout[(x,y-1)].bottom,regular,edges)
        
        else:                                                                                  #  bottom row, any tile but first
            tile = select_tile(layout[(x-1,y)].right, layout[(x,y-1)].bottom,edges,corners)

        layout[(x,y)] = tile
        
        regular = [t for t in regular if t.nbr != tile.nbr]
        edges   = [t for t in edges if t.nbr != tile.nbr]
        corners = [t for t in corners if t.nbr != tile.nbr]
        
        if x == max_x and max_y == len(tiles):
            max_y = ((len(tiles) // (max_x + 1)) - 1)      #  calculate number of rows once we know how many tiles per row
            
        x, y = (0,y+1) if x == max_x else (x+1,y)          #  work through the image left to right, top to bottom
    
    return layout


def select_tile(side_edge, top_edge, tile_style_1, tile_style_2):
    
    n = side_edge if side_edge is not None else top_edge
    matched = False;  tile = ''

    potential_matches = [t for t in tile_style_1 if abs(n) in (abs(t.left), abs(t.top), abs(t.right), abs(t.bottom))
                                                 and abs(n) not in t.outer_edges]
    for t in potential_matches:        
        matched, tile = match_oriented_tile(t,side_edge,top_edge)
        if matched: break
        
    if not matched:
        
        potential_matches = [t for t in tile_style_2 if abs(n) in (abs(t.left), abs(t.top), abs(t.right), abs(t.bottom))
                                                     and abs(n) not in t.outer_edges]
        for t in potential_matches:        
            matched, tile = match_oriented_tile(t,side_edge,top_edge)
            if matched: break
            
    return tile
        
        
def match_oriented_tile(t,x,y):
    
    if x is not None:     #  align left edge to right edge of adjacent target tile and then check top edge matches
        
        if   abs(t.top)    == abs(x): t.rotate(False)
        elif abs(t.bottom) == abs(x): t.rotate()
        elif abs(t.right)  == abs(x): t.flip_y()
        
        if abs(t.left) == abs(x) and y is None:
            y = t.bottom if abs(t.bottom) in t.outer_edges else t.top
        
        if (abs(t.left) == abs(x) and abs(y) == abs(t.bottom)) or (t.left + x == 0): t.flip_x()

    else:                 #  align top edge to bottom edge of adjacent target tile and then check left edge matches
        
        if   abs(t.right)  == abs(y): t.rotate(False)
        elif abs(t.left)   == abs(y): t.rotate()
        elif abs(t.bottom) == abs(y): t.flip_x()
        
        if abs(t.top) == abs(y) and x is None:
            x = t.right if abs(t.right) in t.outer_edges else t.left
        
        if (abs(t.top) == abs(y) and abs(x) == abs(t.right)) or (t.top + y == 0): t.flip_y()
        
    matched = True if t.left == x and t.top == y else False

    return matched, t


def assemble_image(layout):
    
    image = [];  y = 0
    
    while y <= max(layout)[1]:

        image_lines = []
        for t in [v for k,v in sorted(layout.items()) if k[1] == y]:
            t.remove_edges()
            image_lines += [t.detail]            
        for line in zip(*image_lines): 
            image += [''.join(line)]
        y += 1
        
    return Image(1,image,len(image[0]),len(image))


def highlight_monsters(image,monster_signature):
    
    def monster(signature,m,len_x):
        
        monster_regex = ''        
        for i in signature:            
            if type(i) is str:              monster_regex += len(i) * m
            elif type(i) is int and i > 0:  monster_regex += i * '.'
            elif type(i) is int and i <= 0: monster_regex += (len_x + i) * '.'
            
        return monster_regex
    
    pattern = monster(monster_signature,'1',image.len_x)
    
    monsters = []
    for _ in range(2):
        if len(monsters) == 0:
            for _ in range(4):
                monsters = list(set(re.findall(rf'{pattern}',''.join(image.detail))))
                if len(monsters) == 0: image.rotate()
                else: break
        if len(monsters) == 0: image.flip_y()

    while len(monsters) > 0:                     #  Due to using a single line regex against a concatenated string of all lines, matched patterns
                                                 #  can overlap (e.g. 2+ monsters on the same y axis). Updating the image to highlight found monsters      
        highlighted_monsters = []                #  results in any other monsters on the same y axis not being highlighted, hence we may need multiple
        for mon in monsters:                     #  passes to capture them all.
            hilite = ''
            for i,m in enumerate(mon):
                hilite = hilite + '2' if m == '1' and m == pattern[i] else hilite + m
            highlighted_monsters += [hilite]
            
        image_str = ''.join(image.detail)
        for i, monster in enumerate(monsters):
            image_str = re.sub(monster,highlighted_monsters[i],image_str)
        image.detail = [image_str[i:i+image.len_x] for i in range(0,len(image_str),image.len_x)]
        
        monsters = list(set(re.findall(rf'{pattern}',''.join(image.detail))))

    return image


def image_analysis(image,layout,monster_signature):
    
    max_x, max_y = max(layout)
    corner_tile_product = layout[(0,0)].nbr * layout[(0,max_y)].nbr * layout[(max_x,0)].nbr * layout[(max_x,max_y)].nbr
    water_roughness = ''.join(image.detail).count('1')
    monster_ct = ''.join(image.detail).count('2') // len(''.join([x for x in monster_signature if type(x) is str]))
    
    image.render('_^#')
    print('\ncorner tile product:',corner_tile_product)
    print('water roughness:',water_roughness)
    print('sea monsters:',monster_ct)
    
    return (corner_tile_product, water_roughness) 


def main(filepath,tile_size_x,tile_size_y,monster_signature):
    
    edge_lookup = build_lookup(tile_size_x)
    tiles       = categorise_tiles(initialise_tiles(filepath,edge_lookup,tile_size_x,tile_size_y))
    layout      = determine_layout(tiles)
    image       = highlight_monsters(assemble_image(layout),monster_signature)
    summary     = image_analysis(image,layout,monster_signature)

    return summary
        
main('20.txt', 10, 10, ['x',-19,'x',4,'xx',4,'xx',4,'xxx',-19,'x',2,'x',2,'x',2,'x',2,'x',2,'x'])
