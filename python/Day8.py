import pprint
import copy

# Image is 25W x 6H
image_width = 25
image_height = 6
image_size = image_height * image_width


def read_input():
    with open("Day8-input.txt") as f:
        data = f.readline().strip()
    return data


def data_to_layers(data):
    chunks = int(len(data) / image_size)
    assert chunks == 100
    layers = []
    for i in range(0, chunks):
        layers.append(list(data[i * image_size:(i + 1) * image_size]))
    return layers


def part1(layers):
    # find the layer with the least number of 0's
    # Multiply the number of 1's by the number of 2's

    # find layer with least 0's
    least0 = 25 * 6
    least0_layer = None
    for i in range(0, len(layers)):
        count0 = lambda x: len([a for a in layers[i] if a == '0'])
        z = count0(layers[i])
        if z < least0:
            least0 = z
            least0_layer = i
    print("Least 0 layer: {} with {} zeros".format(least0_layer, least0))

    # multiply 1 digits by 2 digits
    count1 = len([a for a in layers[least0_layer] if a == '1'])
    count2 = len([a for a in layers[least0_layer] if a == '2'])
    result = count1*count2
    print("Part1: {}".format(result))
    return


def layer_to_image(layer):
    image = [layer[i * image_width:(i + 1) * image_width] for i in range(0, int(len(layer) / image_width))]
    for y in range(0,len(image)):
        for x in range(0,len(image[y])):
            if image[y][x] == '2' or image[y][x] == '0':
                image[y][x] = '-'
    return image


def print_image(image):
    for i in image:
        print("".join(i))


def combine_layer(top_image, input_layer):
    black = '0'
    white = '1'
    transparent = '2'
    for p in range(0, len(input_layer)):
        if input_layer[p] != transparent and top_image[p] == transparent:
            top_image[p] = input_layer[p]
    return top_image


def part2(layers):
    print("Part 2")
    final_image = copy.deepcopy(layers[0])

    for layer in layers:
        final_image = combine_layer(final_image, layer)

    # square image to 25x6
    image = layer_to_image(final_image)
    print("Final Image")
    print_image(image)





if __name__ == "__main__":
    d = read_input()
    layers = data_to_layers(d)
    part1(layers)

    part2(layers)

    pass
