import random
from .heroes import HEROES

def get_random_hero():
    """Возвращает случайного героя Dota 2."""
    return random.choice(HEROES)

def get_random_heroes(count=1):
    """Возвращает список из N случайных героев."""
    return random.sample(HEROES, count)