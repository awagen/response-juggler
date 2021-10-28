import asyncio
import os
from typing import Tuple, List

import aiohttp
import nest_asyncio

from src.config.env_config import EnvConfig
from src.lib.sampler.selectors.field_sampler_selector import FieldSamplerSelector
from src.lib.sampler.selectors.json_sampler_selector import JsonSamplerSelector
from src.lib.string_utils import StringUtils


class AppConfig:
    RELATIVE_PARTIALS_SUBFOLDER = "./src/templates/partials"
    RELATIVE_TEMPLATES_SUBFOLDER = "./src/templates"
    SETTING_KEY_NUM_CONNECTIONS = "NUM_CONNECTIONS"

    num_connections: int = int(os.getenv(SETTING_KEY_NUM_CONNECTIONS, 100))

    # get those partial names for which all needed env variables are set
    # so we can extract the json content and sampler
    fully_defined_partial_names = EnvConfig.configured_partial_names()

    print("fully defined partial names: %s" % fully_defined_partial_names)

    partial_placeholder_to_content_map = {}
    partial_placeholder_to_sampler_map = {}

    for partial_name in fully_defined_partial_names:
        partial_placeholder = os.getenv(EnvConfig.TEMPLATE_PARTIAL_IDENT_PREFIX + partial_name)
        partial_path = os.getenv(EnvConfig.TEMPLATE_PARTIAL_CONTENT_PREFIX + partial_name)
        with open("%s/%s" % (RELATIVE_PARTIALS_SUBFOLDER, partial_path), "r") as file:
            partial_content = file.read()
            partial_placeholder_to_content_map[partial_placeholder] = partial_content
        partial_name_suffix = "_%s" % partial_name
        suffix_check_func = StringUtils.ends_on_suffix_func("_%s" % partial_name)
        sampler_vars_tmp: List[Tuple[str, str]] = list([(x, os.getenv(x)) for x in os.environ.keys() if
                                                        x.startswith(EnvConfig.PARTIAL_SAMPLER_SETTINGS_PREFIX)])
        sampler_vars = []
        for sampler_var in sampler_vars_tmp:
            if sampler_var[0].endswith(partial_name_suffix):
                sampler_vars.append(sampler_var)

        # set partial sampler (which will always be a json sampler, otherwise would be field and not partial
        partial_placeholder_to_sampler_map[partial_placeholder] = JsonSamplerSelector.select(sampler_vars,
                                                                                             partial_content)

    # set sampler per field to substitute in partial
    field_names = [x.removeprefix(EnvConfig.TEMPLATE_FIELD_IDENT_PREFIX) for x in os.environ.keys() if
                   x.startswith(EnvConfig.TEMPLATE_FIELD_IDENT_PREFIX)]
    field_placeholder_to_sampler_map = {}
    for field_name in field_names:
        field_name_suffix = "_%s" % field_name
        sampler_vars_tmp: List[Tuple[str, str]] = list([(x, os.getenv(x)) for x in os.environ.keys() if
                                                        x.startswith(EnvConfig.FIELD_SAMPLER_SETTINGS_PREFIX)])
        sampler_vars = []
        for sampler_var in sampler_vars_tmp:
            if sampler_var[0].endswith(field_name_suffix):
                sampler_vars.append(sampler_var)
        field_placeholder_to_sampler_map[
            os.getenv(EnvConfig.TEMPLATE_FIELD_IDENT_PREFIX + field_name)] = FieldSamplerSelector.select(sampler_vars)

    # load main content to sample partials in in sampling
    # right now we only allow one main content, might change that by having a map for
    # distinct mains analogue to the partials
    main_path = os.getenv(EnvConfig.MAIN_TEMPLATE_ENV_VAR)
    with open("%s/%s" % (RELATIVE_TEMPLATES_SUBFOLDER, main_path), "r") as file:
        main_template = file.read()

    @staticmethod
    def main_template_content() -> str:
        return AppConfig.main_template

    @staticmethod
    def get_partial_placeholder_to_sampler_map():
        """
        The partial placeholder to sampler map is everything we need to replace
        placeholders for partials
        :return:
        """
        return dict(AppConfig.partial_placeholder_to_sampler_map)

    @staticmethod
    def get_field_placeholder_to_sampler_map():
        """
        The field placeholder to sampler map is everything we need to replace
        single field placeholders with actual values
        :return:
        """
        return dict(AppConfig.field_placeholder_to_sampler_map)

    # setting aiohttp tcp connector, limiting the number of simultaneous connections
    tcp_connector = aiohttp.TCPConnector(limit=num_connections, limit_per_host=num_connections)
    # to be able to start multiple processes utilizing one loop
    # (uvicorn is already starting one up, also need to configure it
    # to utilize the asyncio loop to make the nest_asyncio hack work (see readme))
    nest_asyncio.apply()
    event_loop = asyncio.get_event_loop()
    # utilizing single session to utilize connection pools
    # connector_owner must be set to False here, otherwise subsequent requests will fail
    http_client_session = aiohttp.ClientSession(connector=tcp_connector, loop=event_loop, connector_owner=False)
