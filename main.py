import json
import random
from typing import Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config.app_config import *
from src.config.app_config import AppConfig

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


def replace_placeholders(content: str, replacements: Dict[str, Sampler]) -> (str, bool):
    print("replacements: %s" % replacements)
    did_replace = False
    for placeholder in replacements.keys():
        if placeholder in content:
            did_replace = True
            replacement = replacements[placeholder].sample()
            if isinstance(replacement, list):
                replacement = "[" + ",".join(replacement) + "]"
            else:
                replacement = str(replacement)
            content = content.replace(placeholder, replacement)
    return content, did_replace


@app.get("/search")
async def search():
    # getting the main template
    main_content = AppConfig.main_template_content()
    # replacement samplers for the partials
    partial_placeholder_sampler_map = AppConfig.get_partial_placeholder_to_sampler_map()
    # replacement samplers for the fields
    field_placeholder_sampler_map = AppConfig.get_field_placeholder_to_sampler_map()
    print("field_placeholder_sampler_map: %s" % field_placeholder_sampler_map)
    # now combine both in single placeholder replacement map
    all_placeholder_sampler_map = {**field_placeholder_sampler_map, **partial_placeholder_sampler_map}

    print("main content before replacement: %s" % main_content)

    # now just replace all keys starting from main_content till no placeholder matches anymore
    max_replacement_iterations = 10
    current_iteration = 0
    did_replace = True
    while current_iteration < max_replacement_iterations and did_replace:
        current_iteration += 1
        main_content, did_replace = replace_placeholders(main_content, all_placeholder_sampler_map)

    print("main content after replacement: %s" % main_content)

    # prepping the json
    # doc_array = []
    # for pid in product_id_sample:
    #     doc_array.append(AppConfig.doc_partial.replace(AppConfig.search_replace_pid_key, pid))
    # TODO: we likely will have to add to our list samplers the join below to wrap it in a json list structure
    # doc_array_str = '[' + ','.join(doc_array) + ']'
    # result_content = AppConfig.search_content.replace(AppConfig.search_replace_doc_list_key, doc_array_str)
    # return json.loads(result_content)
    return json.loads(main_content)
