def rotate(image):

     return [] + [''.join([row[i] for row in image][::-1]) for i in range(len(image[0]))]


def get_reflection(image, false_reflection=False, rotation=False):

    image, multiplier = (rotate(image),1) if rotation else (image,100)

    for i in range(1,len(image)):

        chunk = min(i,len(image)-i)
        above = image[i-chunk:i]
        below = image[i:i+chunk][::-1]

        if above == below:
            if (i, multiplier) != false_reflection:
                return (i, multiplier)

    if not rotation:
        return get_reflection(image, false_reflection, True)

    return None


def update_row(image,y,x):

    new_image = [] + image
    updated_row = image[y][:x] + {'.':'#','#':'.'}[image[y][x]] + image[y][x+1:]
    new_image[y] = updated_row

    return new_image


def image_permutations(image):

    return [update_row(image,y,x) for y in range(len(image)) for x in range(len(image[0]))]


def get_true_reflection(image, original_reflection):

    altered_images = image_permutations(image)

    for image in altered_images:

        new_reflection = get_reflection(image, original_reflection)

        if new_reflection and new_reflection != original_reflection:
            return new_reflection

    return None


def sum_reflections(reflections):

    return sum([i*m for i,m in reflections])


def main(filepath):

    images = [x.split('\n') for x in open(filepath).read().split('\n\n')]

    original_reflections  = [get_reflection(image) for image in images]
    true_reflections = [get_true_reflection(i,r) for i,r in zip(images, original_reflections)]

    return sum_reflections(original_reflections), sum_reflections(true_reflections)


print(main('13.txt'))