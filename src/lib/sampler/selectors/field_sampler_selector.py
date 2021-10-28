from typing import List, Tuple

from src.lib.sampler.list_sampler import ListSampler
from src.lib.sampler.one_of_sampler import OneOfSampler
from src.lib.sampler.type_conversions import TypeConversions


class FieldSamplerSelector:
    # field sampling can be single values of type SINGLE or LIST
    # in each case takes a comma-separated list of samples to select from
    FIELD_SAMPLER_TYPE_SINGLE = "SINGLE"
    FIELD_SAMPLER_TYPE_LIST = "LIST"
    # repeat setting only relevant for list, e.g whether sampling shall repeat elements
    FIELD_SAMPLER_TYPE_LIST_REPEAT_PREFIX = "RESPONSE_FIELD_SAMPLER_REPEAT_"
    FIELD_SAMPLER_SELECTION_PREFIX = "RESPONSE_FIELD_SAMPLER_SELECTION_"
    FIELD_SAMPLER_ELEMENT_CAST_PREFIX = "RESPONSE_FIELD_SAMPLER_ELEMENT_CAST_"
    FIELD_SAMPLER_TYPE_PREFIX = "RESPONSE_FIELD_SAMPLER_TYPE_"
    FIELD_SAMPLER_LIST_MIN_NUM_PREFIX = "RESPONSE_PARTIAL_SAMPLER_MIN_NUM_"
    FIELD_SAMPLER_LIST_MAX_NUM_PREFIX = "RESPONSE_PARTIAL_SAMPLER_MAX_NUM_"

    @staticmethod
    def select(relevant_vars: List[Tuple[str, str]]):
        """
        Samples single fields based on settings picked from environment variables.
        Either randomly selects one of the values passed by comma-separated list by the selection
        env variable, or samples a list with or without possible repetition of values.
        Further, the cast setting allows to define a value cast, from string to int, float or bool (or leave as is)
        :param relevant_vars:
        :return:
        """
        s_type = [x[1] for x in relevant_vars if x[0].startswith(FieldSamplerSelector.
                                                                 FIELD_SAMPLER_TYPE_PREFIX)][0]
        selection: List[any] = [x[1] for x in relevant_vars if x[0].startswith(FieldSamplerSelector.
                                                                               FIELD_SAMPLER_SELECTION_PREFIX)][
            0].split(",")
        type_conversion = [x[1] for x in relevant_vars if x[0].startswith(FieldSamplerSelector.
                                                                          FIELD_SAMPLER_ELEMENT_CAST_PREFIX)][0]
        selection = list([TypeConversions.convert(x, type_conversion) for x in selection])
        if s_type == FieldSamplerSelector.FIELD_SAMPLER_TYPE_SINGLE:
            return OneOfSampler(selection, 1000)
        elif s_type == FieldSamplerSelector.FIELD_SAMPLER_TYPE_LIST:
            do_repeat = [bool(x[1]) for x in relevant_vars if x[0].startswith(FieldSamplerSelector.
                                                                              FIELD_SAMPLER_TYPE_LIST_REPEAT_PREFIX)][
                0]
            min_num = [int(x[1]) for x in relevant_vars if x[0].startswith(FieldSamplerSelector.
                                                                           FIELD_SAMPLER_LIST_MIN_NUM_PREFIX)][
                0]
            max_num = [int(x[1]) for x in relevant_vars if x[0].startswith(FieldSamplerSelector.
                                                                           FIELD_SAMPLER_LIST_MAX_NUM_PREFIX)][
                0]

            return ListSampler(selection, min_num=min_num, max_num=max_num, with_putback=do_repeat)