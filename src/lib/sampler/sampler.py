from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')


class Sampler(ABC, Generic[T]):

    @abstractmethod
    def sample(self) -> T:
        pass
