
max_width, max_height = 1500, 900
std_ratio = max_width / max_height


def resize_by_height(height, wh_ratio):
    ratio = height / max_height
    width = max_height * wh_ratio
    return (int(width), max_height), ratio


def resize_by_width(width, wh_ratio):
    ratio = width / max_width
    height = max_width / wh_ratio
    return (max_width, int(height)), ratio


def resize(width, height):
    wh_ratio = width / height

    if wh_ratio > std_ratio:
        return resize_by_width(width, wh_ratio)
    else:
        return resize_by_height(height, wh_ratio)


if __name__ == '__main__':
    (w, h), r = resize(1600, 1200)
    print(w, h, r)
