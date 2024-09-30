import logging
import os

import httpx
import uvicorn
from cli import init_settings, process_query
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

    response, span_id = process_query(query, query_engine_type, prompt)

    return {"response": response, "span_id": span_id}


@app.post("/api/feedback")
async def submit_feedback(request: Request):
    """
    This function handles POST requests to the '/api/feedback' endpoint.
    It receives a FastAPI Request object containing feedback data for a specific span ID.

    Parameters:
    request (Request): A FastAPI Request object containing the incoming request.
        It is expected to have the following parameters in the JSON body:
        - 'span_id' (str): The span ID for which feedback is being submitted.
        - 'is_positive' (bool): A boolean indicating whether the feedback is positive (True) or negative (False).

    Returns:
    dict: A JSON response with the following structure:
        - 'message' (str): A confirmation message indicating the feedback was received.
        - 'error' (str, optional): An error message if an error occurred during processing.
    """
    try:
        body = await request.json()
        span_id = body.get("span_id")
        is_positive = body.get("is_positive")

        if span_id is None or is_positive is None:
            logger.error("Missing required parameters in feedback request")
            return {
                "error": "Missing required parameters. Both 'spanId' and 'isPositive' must be provided."
            }

        logger.info(
            f"Received feedback for span ID {span_id}: {'Positive' if is_positive else 'Negative'}"
        )

        client = httpx.Client()
        phoenix_endpoint = os.getenv("ARIZE_PHOENIX_ENDPOINT").strip()

        annotation_payload = {
            "data": [
                {
                    "span_id": span_id,
                    "name": "user feedback",
                    "annotator_kind": "HUMAN",
                    "result": {
                        "label": "thumbs-up",
                        "score": 1 if is_positive else 0,
                    },
                }
            ]
        }

        try:
            response = client.post(
                f"{phoenix_endpoint}/v1/span_annotations?sync=false",
                json=annotation_payload,
            )

            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error occurred while sending feedback to Phoenix: {e}")
        except Exception as e:
            logger.error(
                f"An error occurred while sending feedback to Phoenix: {str(e)}"
            )

        return {"message": f"Feedback received for span ID {span_id}"}
    except Exception as e:
        logger.error(f"Error processing feedback: {str(e)}")
        return {"error": "An error occurred while processing the feedback"}


if __name__ == "__main__":
    app_host = os.getenv("APP_HOST", "0.0.0.0")
    app_port = int(os.getenv("APP_PORT", 8000))
    app_workers = int(os.getenv("APP_WORKERS", 4))
    reload = True if environment == "dev" else False

    logger.info(f"Starting FastAPI server on {app_host}:{app_port}")

    uvicorn.run(
        app="api:app", host=app_host, port=app_port, reload=reload, workers=app_workers
    )
