def chunks(iterable, size=1):
    l = len(iterable)
    for index in range(0, l, size):
        yield iterable[index:min(index + size, l)]


def rgb_to_hex(r, g, b):
    return '#%02x%02x%02x' % (int(r * 255), int(g * 255), int(b * 255))
