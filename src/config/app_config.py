import asyncio
import os

import aiohttp
import nest_asyncio


class AppConfig:
    num_connections: int = int(os.getenv("NUM_CONNECTIONS", 100))

    # search endpoint settings
    search_min_products: int = int(os.getenv("RESPONSE_SEARCH_MIN_PRODUCTS", 5))
    search_max_products: int = int(os.getenv("RESPONSE_SEARCH_MAX_PRODUCTS", 20))
    search_replace_doc_list_key = os.getenv("RESPONSE_SEARCH_VAR_DOCS_KEY", "")
    search_replace_pid_key = os.getenv("RESPONSE_SEARCH_VAR_PID_KEY", "")
    search_sample_pid: list[str] = os.getenv("RESPONSE_SEARCH_VAR_PID_SAMPLE", "").split(",")
    search_response_template = os.getenv("RESPONSE_SEARCH_TEMPLATE", "searchresponse.json")
    search_doc_partial = os.getenv("RESPONSE_SEARCH_DOC_PARTIAL", "doc.json")

    # partial for single documents
    with open("./src/templates/partials/%s" % search_doc_partial, "r") as file:
        doc_partial = file.read()

    # main search result, needing to replace
    with open("./src/templates/%s" % search_response_template, "r") as file:
        search_content: str = file.read()

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
