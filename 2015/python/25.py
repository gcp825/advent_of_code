def main(code,y,x):
    
    target_diagonal = y+x-1
    codes = sum(range(2,target_diagonal)) + x
    for _ in range(codes):
        code = (code*252533) % 33554393
    return code

print(main(20151125,2981,3075))
