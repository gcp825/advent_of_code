def main(input):

    recipes, indices, pt1_idx = ('37', (0,1), int(input))

    while input not in recipes[-7:]:

        recipes += str(sum([int(recipes[i]) for i in indices]))
        indices = tuple([(indices[i]+int(recipes[indices[i]])+1)%len(recipes) for i in (0,1)])

    return int(recipes[pt1_idx:pt1_idx+10]), recipes.find(input)

print(main('030121'))