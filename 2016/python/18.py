def main(rows,tiles):
    
    safe_ct = tiles.count('.')
    row = ['.'] + list(tiles) + ['.']
    traps = list((list('^^.'), list('.^^'), list('^..'), list('..^')))
    row_length = len(row) - 1

    for _ in range(rows-1):
        row =  ['.'] + ['^' if row[i-1:i+2] in traps else '.' for i in range(1,row_length)] + ['.']
        safe_ct += row.count('.')-2
 
    return safe_ct   

start_row = '^.....^.^^^^^.^..^^.^.......^^..^^^..^^^^..^.^^.^.^....^^...^^.^^.^...^^.^^^^..^^.....^.^...^.^.^^.^'
print(main(40,start_row))
print(main(400000,start_row))
