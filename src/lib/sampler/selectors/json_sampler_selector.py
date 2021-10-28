from typing import Tuple, List

from src.lib.sampler.list_sampler import ListSampler
from src.lib.sampler.one_of_sampler import OneOfSampler


class JsonSamplerSelector:
    JSON_SAMPLER_TYPE_SINGLE = "SINGLE"
    JSON_SAMPLER_TYPE_LIST = "LIST"
    PARTIAL_SAMPLER_TYPE_PREFIX = "RESPONSE_PARTIAL_SAMPLER_TYPE_"
    PARTIAL_SAMPLER_LIST_MIN_NUM_PREFIX = "RESPONSE_PARTIAL_SAMPLER_MIN_NUM_"
    PARTIAL_SAMPLER_LIST_MAX_NUM_PREFIX = "RESPONSE_PARTIAL_SAMPLER_MAX_NUM_"

    @staticmethod
    def select(relevant_vars: List[Tuple[str, str]], json_content: str):
        """
        Here we sample json partials, so can either be single or list of the same json partial
        (further nested json would be single partial json that contains further partials).
        :param relevant_vars:
        :param json_content: the json to duplicate or just return as is, based on the sampler type
        :return:
        """
        s_type = [x[1] for x in relevant_vars if x[0].startswith(JsonSamplerSelector.
                                                                 PARTIAL_SAMPLER_TYPE_PREFIX)][0]
        if s_type == JsonSamplerSelector.JSON_SAMPLER_TYPE_SINGLE:
            return OneOfSampler([json_content])
        if s_type == JsonSamplerSelector.JSON_SAMPLER_TYPE_LIST:
            min_num = [int(x[1]) for x in relevant_vars if x[0].startswith(JsonSamplerSelector.
                                                                           PARTIAL_SAMPLER_LIST_MIN_NUM_PREFIX)][
                0]
            max_num = [int(x[1]) for x in relevant_vars if x[0].startswith(JsonSamplerSelector.
                                                                           PARTIAL_SAMPLER_LIST_MAX_NUM_PREFIX)][
                0]
            return ListSampler[List[str]]([json_content], min_num=min_num, max_num=max_num, with_putback=True)
