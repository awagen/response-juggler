import random
from typing import TypeVar, List, Callable

from src.lib.sampler.sampler import Sampler

T = TypeVar('T')


class ListSampler(Sampler[List[T]]):

    def __init__(self, selection: List[T], min_num: int, max_num: int, with_putback: bool):
        """
        Simple list sampler that either samples with or without replacement
        :param selection:
        :param min_num:
        :param max_num:
        :param with_putback:
        """
        self.min_num = max(0, min_num)
        self.sample_fun: Callable[[List[T], int], List[T]]
        if with_putback:
            self.max_num = max_num
            self.sample_fun = lambda x, y: random.choices(x, k=y)
        else:
            self.max_num = min(len(selection), max_num)
            self.sample_fun = lambda x, y: random.sample(x, k=y)
        self.selection = selection

    def sample(self) -> List[T]:
        num: int = random.choice(range(self.min_num, self.max_num + 1))
        return self.sample_fun(self.selection, num)
