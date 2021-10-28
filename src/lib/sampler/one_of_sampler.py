import random
from typing import TypeVar, List

from src.lib.sampler.sampler import Sampler

T = TypeVar('T')


class OneOfSampler(Sampler[T]):

    def __init__(self, selection: List[T]):
        self.selection = selection
        self.random_gen = random.Random(500)

    def sample(self) -> T:
        print("selecting out of selection: %s" % self.selection)
        # TODO: both of choice and saple are not great since they depend on system time and will thus generate same
        # values for close enough calls
        #selected = self.random_gen.choice(self.selection)
        selected = random.sample(self.selection, k=1)[0]
        print("selected: %s" % selected)
        return selected
