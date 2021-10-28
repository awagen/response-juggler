import random
from typing import TypeVar, List

from src.lib.sampler.sampler import Sampler

T = TypeVar('T')


class OneOfSampler(Sampler[T]):

    def __init__(self, selection: List[T], pre_sample_size: int):
        self.selection = selection
        self.pre_sample = random.choices(selection, k=pre_sample_size)
        self.random_gen = random.Random()
        self.random_gen.seed(500)

    def sample(self) -> T:
        """
        both random.choice and random.sample depend on system time, and thus will generate same values for calls
        very close to each other. To circumvent this, we keep a pre-sampling that is refilled every time an element
        is picked.
        :return:
        """
        selected = self.pre_sample.pop(0)
        self.pre_sample.append(random.choice(self.selection))
        return selected
