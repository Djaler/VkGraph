def chunks(iterable, size=1):
    l = len(iterable)
    for index in range(0, l, size):
        yield iterable[index:min(index + size, l)]
