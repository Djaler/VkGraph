from random import randint

from app.services.temperature_map import calculate_color


def test_red():
    for _ in range(10):
        interval = randint(1, 1000)
        value = interval
        
        color = calculate_color(value, interval)
        
        assert color == "#ff0000"


def test_yellow():
    for _ in range(10):
        interval = randint(1, 1000) * 4
        value = interval * 3 / 4
        
        color = calculate_color(value, interval)
        
        assert color == "#ffff00"


def test_green():
    for _ in range(10):
        value = randint(1, 1000)
        interval = value * 2
        
        color = calculate_color(value, interval)
        
        assert color == "#00ff00"


def test_blue():
    for _ in range(10):
        value = randint(1, 1000)
        interval = value * 4
        
        color = calculate_color(value, interval)
        
        assert color == "#00ffff"


def test_dark_blue():
    for _ in range(10):
        interval = randint(1, 1000)
        
        color = calculate_color(0, interval)
        
        assert color == "#0000ff"


def test_empty_interval():
    for _ in range(10):
        value = randint(1, 1000)
        
        color = calculate_color(value, 0)
        
        assert color == "#ff0000"
