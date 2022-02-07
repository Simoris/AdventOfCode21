import numpy as np


def load_and_process_data(path):
    file = open(path, "r")
    data = file.read()
    data = data.split('\n\n')
    enh = [1 if char == '#' else 0 for char in data[0]]
    img = np.array([[1 if char == '#' else 0 for char in line] for line in data[1].split('\n')])
    return enh, img


def pad(img, size_padding=1):
    x, y = img.shape
    pad_img = np.zeros((x + 2*size_padding, y + 2*size_padding), dtype=int)
    pad_img[size_padding:x + size_padding, size_padding:y + size_padding] = img
    return pad_img


def fix_outer_line(img, value):
    img[0, :] = value
    img[-1, :] = value
    img[:, -1] = value
    img[:, 0] = value
    return img


def get_num_from_img(matrix):
    return int(''.join([str(x) for x in np.reshape(matrix, 9)]), 2)


def enhance(img, enh):
    x, y = img.shape
    new_img = img.copy()
    for i in range(x-2):
        for j in range(y-2):
            new_img[i+1, j+1] = enh[get_num_from_img(img[i:i+3, j:j+3])]
    return new_img


def task1():
    enh, img = load_and_process_data("input/day20.txt")
    img = pad(img, 4)
    for i in range(1):
        img = enhance(img, enh)
        img = fix_outer_line(img, enh[0])
        img = enhance(img, enh)
        img = fix_outer_line(img, enh[-1])
    print(np.sum(img))


def task1():
    enh, img = load_and_process_data("input/day20.txt")
    img = pad(img, 100)
    for i in range(25):
        img = enhance(img, enh)
        img = fix_outer_line(img, enh[0])
        img = enhance(img, enh)
        img = fix_outer_line(img, enh[-1])
    print(np.sum(img))
