import argparse
import datetime
import json
import os
import uuid

import nest_asyncio
from dotenv import load_dotenv
from llama_index.core import (
    Document,
    PromptTemplate,
    QueryBundle,
    Settings,
    VectorStoreIndex,
)
from llama_index.core.evaluation import RelevancyEvaluator
from llama_index.core.extractors import (
    KeywordExtractor,
    QuestionsAnsweredExtractor,
    SummaryExtractor,
    TitleExtractor,
)
from llama_index.core.indices.query.query_transform import HyDEQueryTransform
from llama_index.core.ingestion import IngestionCache, IngestionPipeline
from llama_index.core.query_engine import RetryQueryEngine, TransformQueryEngine
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.extractors.entity import EntityExtractor
from llama_index.llms.ollama.base import DEFAULT_REQUEST_TIMEOUT, Ollama
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

load_dotenv()
nest_asyncio.apply()


def main():
    init_settings()

    parser = argparse.ArgumentParser(
        description="Index and query school records using LlamaIndex and Elasticsearch."
    )
    parser.add_argument("-i", "--index", action="store_true", help="Create a new index")
    parser.add_argument(
        "-c", "--chat", action="store_true", help="Chat with the documents"
    )
    parser.add_argument(
        "-e", "--export", type=str, help="Export processed data to given directory"
    )
    args = parser.parse_args()

    if args.index:
        print("Running ingestion pipeline...")
        run_ingestion_pipeline()
        print("Index created successfully.")
    elif args.chat:
        print("Starting chat session...")
        run_chat_session()
        print("Chat session ended.")
    elif args.export:
        print("Exporting processed data...")
        run_export(args.export)
        print("Export completed successfully.")


def init_settings():
    base_url = os.getenv("OLLAMA_URL") or "http://127.0.0.1:11434"
    request_timeout = float(
        os.getenv("OLLAMA_REQUEST_TIMEOUT", DEFAULT_REQUEST_TIMEOUT)
    )

    Settings.embed_model = OllamaEmbedding(
        base_url=base_url,
        model_name=os.getenv("EMBEDDING_MODEL"),
    )
    Settings.llm = Ollama(
        base_url=base_url, model=os.getenv("MODEL"), request_timeout=request_timeout
    )

    Settings.chunk_size = int(os.getenv("CHUNK_SIZE", "512"))
    Settings.chunk_overlap = int(os.getenv("CHUNK_OVERLAP", "32"))


def run_ingestion_pipeline():
    pipeline = IngestionPipeline(
        transformations=[
            get_document_splitter(),
            EntityExtractor(
                prediction_threshold=0.6, label_entities=True, device="mps"
            ),
            TitleExtractor(nodes=2),
            QuestionsAnsweredExtractor(questions=3),
            SummaryExtractor(summaries=["prev", "self"], llm=Settings.llm),
            KeywordExtractor(keywords=5),
            Settings.embed_model,
        ],
        cache=IngestionCache(),
        vector_store=get_vector_store(),
    )
    pipeline.run(documents=get_documents(), show_progress=True)


def get_document_splitter():
    use_semantic = os.getenv("USE_SEMANTIC_SPLITTER", "True").lower

    if use_semantic == "true":
        from llama_index.core.node_parser import SemanticSplitterNodeParser

        buffer_size = int(os.getenv("SEMANTIC_SPLITTER_BUFFER_SIZE", "1"))
        breakpoint_percentile_threshold = int(
            os.getenv("SEMANTIC_SPLITTER_BREAKPOINT_PERCENTILE_THRESHOLD", "95")
        )

        return SemanticSplitterNodeParser(
            buffer_size=buffer_size,
            breakpoint_percentile_threshold=breakpoint_percentile_threshold,
            embed_model=Settings.embed_model,
        )
    else:
        from llama_index.core.node_parser import SentenceSplitter

        return SentenceSplitter(
            chunk_size=Settings.chunk_size, chunk_overlap=Settings.chunk_overlap
        )


def get_vector_store():
    client = get_qdrant_client()
    collection_name = get_collection_name() or f"llama-index-{uuid.uuid4()}"

    return QdrantVectorStore(client=client, collection_name=collection_name)


def get_qdrant_client():
    url = os.getenv("VECTOR_STORE_URL") or "http://localhost"
    port = int(os.getenv("VECTOR_STORE_PORT", 6333))

    return QdrantClient(url=url, port=port)


def get_collection_name():
    return os.getenv("VECTOR_STORE_COLLECTION_NAME")


def get_documents():
    data_path = os.getenv("DATA_PATH") or "data/1_interim/records/json"

    documents = []

    json_files = [f for f in os.listdir(data_path) if f.endswith(".json")]
    for file in json_files:
        with open(os.path.join(data_path, file), "r") as f:
            data = json.load(f)
            metadata = dict(
                file=file,
                school=data["Name of School"][0],
                # teachers=data.get("Teachers", "Unknown"),
            )
            document = Document(text=data["text"], metadata=metadata)
            documents.append(document)

    return documents


def run_chat_session():
    vector_store = get_vector_store()
    index = VectorStoreIndex.from_vector_store(vector_store)

    prompt_path = os.getenv("PROMPT_PATH") or "data/0_raw/prompt.txt"
    with open(prompt_path, "r") as file:
        prompt = file.read()

    prompt_template = PromptTemplate(prompt)

    base_query_engine = index.as_query_engine(
        streaming=True,
        similarity_top_k=int(os.getenv("TOP_K", "10")),
        text_qa_template=prompt_template,
        verbose=True,
    )

    query_response_evaluator = RelevancyEvaluator()
    retry_query_engine = RetryQueryEngine(base_query_engine, query_response_evaluator)

    hyde = HyDEQueryTransform(include_original=True)
    hyde_query_engine = TransformQueryEngine(base_query_engine, hyde)

    try:
        while True:
            print()
            query = input("Researcher: ")
            multi_query = input("Use multi-step queries? (y/[n]): ")

            query_bundle = QueryBundle(
                query, embedding=Settings.embed_model.get_query_embedding(query)
            )

            if multi_query.lower() == "y":
                response = hyde_query_engine.query(query_bundle)
            else:
                response = base_query_engine.query(query_bundle)

            print_response(response)

            retry_query = input("Retry query? (y/[n]): ")
            if retry_query.lower() == "y":
                response = retry_query_engine.query(query_bundle)

                print_response(response)
    except (EOFError, KeyboardInterrupt):
        print("Exiting...")
        pass


def print_response(response):
    print(f"RAG {response.source_nodes[0].score:.3f}:", response)
    print()


def run_export(directory: str):
    client = get_qdrant_client()
    collection_name = get_collection_name()

    records, _ = client.scroll(collection_name, limit=1000)
    payload = [record.payload for record in records]

    os.makedirs(directory, exist_ok=True)
    output_file = (
        f"processed_data_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.json"
    )
    with open(os.path.join(directory, output_file), "w") as f:
        json.dump(payload, f, indent=4)

    print(f"Processed data exported to {output_file}")


if __name__ == "__main__":
    main()
