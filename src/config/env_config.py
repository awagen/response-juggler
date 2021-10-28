import os
from typing import List


class EnvConfig:
    TEMPLATE_PARTIAL_IDENT_PREFIX = "RESPONSE_PARTIAL_IDENT_"
    TEMPLATE_PARTIAL_CONTENT_PREFIX = "RESPONSE_PARTIAL_CONTENT_"
    TEMPLATE_PARTIAL_SAMPLER_TYPE_PREFIX = "RESPONSE_PARTIAL_SAMPLER_TYPE_"
    PARTIAL_SAMPLER_SETTINGS_PREFIX = "RESPONSE_PARTIAL_SAMPLER_"
    TEMPLATE_FIELD_IDENT_PREFIX = "RESPONSE_FIELD_IDENT_"
    TEMPLATE_FIELD_SAMPLER_TYPE_PREFIX = "RESPONSE_FIELD_SAMPLER_TYPE_"
    FIELD_SAMPLER_SETTINGS_PREFIX = "RESPONSE_FIELD_SAMPLER_"
    MAIN_TEMPLATE_ENV_VAR = "RESPONSE_MAIN_TEMPLATE"

    @staticmethod
    def suffixes_for_key(prefix: str):
        return list([x.removeprefix(prefix) for x in os.environ.keys() if
                     x.startswith(prefix)])

    # prepare all partial contents to retrieve them later
    # partial for single documents
    # extract all keys pointing to a partial
    @staticmethod
    def partial_ident_names() -> List[str]:
        """
        Extract for which partial names there is a placeholder defined.
        The placeholder for the partial name is then contained in env var with name
        TEMPLATE_PARTIAL_IDENT_PREFIX + name
        :return:
        """
        return EnvConfig.suffixes_for_key(EnvConfig.TEMPLATE_PARTIAL_IDENT_PREFIX)

    @staticmethod
    def partial_content_names():
        """
        Extract for which partial names there is a content defined.
        The content path for the partial name is then contained in env var with name
        TEMPLATE_PARTIAL_CONTENT_PREFIX + name
        :return:
        """
        return EnvConfig.suffixes_for_key(EnvConfig.TEMPLATE_PARTIAL_CONTENT_PREFIX)

    @staticmethod
    def partial_sampler_names():
        """
        Extract for which partial names there is a sampler type defined.
        The sampler type for the partial name is then contained in env var of name
        TEMPLATE_PARTIAL_SAMPLER_TYPE_PREFIX + name
        :return:
        """
        return EnvConfig.suffixes_for_key(EnvConfig.TEMPLATE_PARTIAL_SAMPLER_TYPE_PREFIX)

    @staticmethod
    def configured_partial_names():
        """
        we only use those partial names for which identifier, content and sampler are defined
        :return:
        """
        return list(
            set(EnvConfig.partial_ident_names()) &
            set(EnvConfig.partial_content_names()) &
            set(EnvConfig.partial_sampler_names()))
