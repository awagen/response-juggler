import json
import random

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


@app.get("/search")
async def search():
    # sampling of product ids from the valid values defined in config
    select_n: int = random.sample(range(AppConfig.search_min_products, AppConfig.search_max_products, 1), 1)[0]
    product_id_sample: list[str] = random.sample(AppConfig.search_sample_pid, select_n)
    # prepping the json
    doc_array = []
    for pid in product_id_sample:
        doc_array.append(AppConfig.doc_partial.replace(AppConfig.search_replace_pid_key, pid))
    doc_array_str = '[' + ','.join(doc_array) + ']'
    result_content = AppConfig.search_content.replace(AppConfig.search_replace_doc_list_key, doc_array_str)
    return json.loads(result_content)
