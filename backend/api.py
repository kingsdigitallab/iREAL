import logging
import os

import uvicorn
from cli import init_settings, process_query
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

load_dotenv()

app = FastAPI()

init_settings()

environment = os.getenv("ENVIRONMENT", "dev")
logger = logging.getLogger("uvicorn")


@app.get("/")
async def redirect_to_docs():
    return RedirectResponse(url="/docs")


@app.post("/api/query")
async def query_api(request: Request):
    """
        This function handles POST requests to the '/api/query' endpoint.
        It receives a FastAPI Request object containing a query parameter,
        prints the query, and returns a JSON response with an empty list of results.

        Parameters:
        request (Request): A FastAPI Request object containing the incoming request.
            It is expected to have the following parameters:
            - 'q' (str): The query to be processed.
            - 'query_engine_type' (str): The query engine to be used for processing the query.
            - 'prompt' (str): The prompt to be used for processing the query.

        Returns:
    dict: A JSON response with the following structure:
            - 'response' (str): The answer generated from processing the query.
                Each response is a list of dictionaries containing:
                - 'source_nodes' (list): A list of source nodes used to generate the response.
                    Each source node is a dictionary containing:
                    - 'node' (dict): Information about the source node, including:
                        - 'id_' (str): Unique identifier for the node.
                        - 'metadata' (dict): Metadata associated with the node.
                        - 'text' (str): The text content of the node.
                        - 'start_char_idx' (int): Starting character index of the text.
                        - 'end_char_idx' (int): Ending character index of the text.
                    - 'score' (float): Relevance score of the source node.
            - 'error' (str, optional): An error message if an error occurred during processing.
    """
    body = await request.json()
    query = body.get("q")
    query_engine_type = body.get("query_engine_type")
    prompt = body.get("prompt")

    logger.info(f"Received query: {query}")
    logger.debug(f"Received query engine: {query_engine_type}")
    logger.debug(f"Received prompt: {prompt}")

    if not query:
        logger.error("No query provided in request")
        return {"error": "No query provided in request"}

    return process_query(query, query_engine_type, prompt)


if __name__ == "__main__":
    app_host = os.getenv("APP_HOST", "0.0.0.0")
    app_port = int(os.getenv("APP_PORT", 8000))
    app_workers = int(os.getenv("APP_WORKERS", 4))
    reload = True if environment == "dev" else False

    logger.info(f"Starting FastAPI server on {app_host}:{app_port}")

    uvicorn.run(
        app="api:app", host=app_host, port=app_port, reload=reload, workers=app_workers
    )
