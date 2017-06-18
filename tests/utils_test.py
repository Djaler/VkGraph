from random import randint

from math import ceil

from app import utils


def test_chunks():
    start = randint(0, 1000)
    end = start + randint(1, 1000)
    step = randint(1, 10)
    iterable = list(range(start, end, step))
    size = randint(1, 10)
    
    chunks = list(utils.chunks(iterable, size))
    
    assert len(chunks) == ceil(len(iterable) / size)
    assert all(len(chunk) == size for chunk in chunks[:-1])
    assert len(chunks[-1]) <= size
    assert iterable == [item for chunk in chunks for item in chunk]


def test_chunks_with_empty_iterable():
    iterable = []
    size = randint(1, 10)
    
    chunks = list(utils.chunks(iterable, size))
    
    assert list(chunks) == []
