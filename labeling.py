import sys
from glob import glob
from os.path import basename, join, isfile

from GUI import GUI


def get_images(input_dir):
    extensions = ['.jpg', '.jpeg', '.png']
    img_paths = []
    for ext in extensions:
        img_paths.extend(glob(input_dir + '/*' + ext))
    return img_paths


def get_start_idx(paths, start=''):
    try:
        start_idx = paths.index(start)
    except ValueError as err:
        start_idx = 0

    return start_idx


def process(img_dir, start=''):
    img_paths = get_images(img_dir)

    img_start = join(img_dir, start)
    idx = get_start_idx(img_paths, img_start)

    while True:
        gui = GUI(img_paths[idx])
        _, pointer = gui.run()
        if pointer == 'p':
            idx = idx - 1 if idx > 0 else len(img_paths) - 1
        elif pointer == 'x':
            break
        else:
            idx = idx + 1 if idx < (len(img_paths) - 1) else 0

    return basename(img_paths[idx])


def read_start_img():
    if isfile('logs.txt'):
        f = open('logs.txt', 'r')
        text = f.read()
        f.close()

        try:
            start = text.split()[-1]
        except IndexError as err:
            start = ''
    else:
        f = open('logs.txt', 'x')
        f.close()
        start = ''

    return start


def write_end_img(end):
    f = open('logs.txt', 'w')
    f.write(end)
    f.write('\n')
    f.close()


def main():
    start = read_start_img()
    if len(sys.argv) > 2:
        start = sys.argv[2]

    cur = process(sys.argv[1], start=start)

    write_end_img(cur)


if __name__ == '__main__':
    main()
