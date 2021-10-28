from typing import Callable


class StringUtils:

    @staticmethod
    def ends_on_suffix_func(name_suffix: str) -> Callable[[str], bool]:
        return lambda x: x.endswith(name_suffix)
