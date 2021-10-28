import json
from typing import Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config.app_config import *
from src.config.app_config import AppConfig
from src.lib.sampler.sampler import Sampler

app = FastAPI()

# cors settings: https://fastapi.tiangolo.com/tutorial/cors/
allowed_origins = os.getenv("allowed_origins", "*")

origins = list([x.strip() for x in allowed_origins.strip().split(",")])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event("shutdown")
async def shutdown():
    await AppConfig.http_client_session.close()
    AppConfig.event_loop.close()


@app.get("/")
async def root():
    return {"message": "hi"}


def apply_replacement_if_applicable(content: str, key: str, sampler: Sampler) -> (str, bool):
    if key in content:
        replacement = sampler.sample()
        if isinstance(replacement, list):
            replacement = "[" + ",".join(replacement) + "]"
        else:
            replacement = str(replacement)
        content = content.replace(key, replacement, 1)
        return content, True
    return content, False


def replace_placeholders(content: str, partial_replacements: Dict[str, Sampler],
                         field_replacements: Dict[str, Sampler]) -> (str, bool, bool):
    """
    replace replacements in content and return resulting content
    :param content: content to replace placeholders in
    :param partial_replacements: the partial replacements (e.g replacing placeholders with jsons)
    :param field_replacements: the field replacements (e.g replacing placeholders with values)
    :return: returns tuple of (new content, is_partial_replacement, is_field_replacement)
    """
    did_partial_replace = False
    did_field_replace = False

    for placeholder in partial_replacements:
        content, did_partial_replace = apply_replacement_if_applicable(content, key=placeholder,
                                                                       sampler=partial_replacements[placeholder])

    for placeholder in field_replacements:
        while True:
            content, did_field_replace = apply_replacement_if_applicable(content, key=placeholder,
                                                                         sampler=field_replacements[placeholder])
            if not did_field_replace:
                break
    return content, did_partial_replace, did_field_replace


@app.get("/search")
async def search():
    # getting the main template
    main_content = AppConfig.main_template_content()
    # replacement samplers for the partials
    partial_placeholder_sampler_map = AppConfig.get_partial_placeholder_to_sampler_map()
    # replacement samplers for the fields
    field_placeholder_sampler_map = AppConfig.get_field_placeholder_to_sampler_map()

    # now just replace all keys starting from main_content till no placeholder matches anymore
    max_replacement_iterations = 10
    current_iteration = 0
    did_replace = True
    while current_iteration < max_replacement_iterations and did_replace:
        main_content, did_partial_replace, did_field_replace = replace_placeholders(main_content,
                                                                                    partial_placeholder_sampler_map,
                                                                                    field_placeholder_sampler_map)
        if did_partial_replace:
            current_iteration += 1
        did_replace = did_partial_replace or did_field_replace

    return json.loads(main_content)
