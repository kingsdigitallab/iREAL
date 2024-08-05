from functools import lru_cache
import numpy as np
import pandas as pd

from typing import Any, Dict, List, Optional, Sequence

from llama_index.core.async_utils import DEFAULT_NUM_WORKERS, run_jobs
from llama_index.core.bridge.pydantic import Field
from llama_index.core.extractors.interface import BaseExtractor
from llama_index.core.llms.llm import LLM
from llama_index.core.prompts import PromptTemplate
from llama_index.core.schema import BaseNode, TextNode, TransformComponent
from llama_index.core.service_context_elements.llm_predictor import LLMPredictorType
from llama_index.core.settings import Settings


DEFAULT_TOPIC_EXTRACT_TEMPLATE = """
You are a text classification expert. Your task is to assign short,
generic topic labels to the following text about Indigenous schools in
NSW, Australia in the late 19th and early 20th century. Use only the
following topics: education policies, assimilation, cultural 
suppression, mission schools, government schools, Aboriginal reserves,
segregation, curriculum, language preservation, traditional knowledge,
teacher training, attendance rates, funding issues, racism, health
conditions, living conditions, vocational training, religious
instruction, child removal policies, Indigenous resistance.
{context_str}. Give {topics} unique topics for this document.
Format as comma separated. Topics: """


class TopicExtractor(BaseExtractor):
    """Topic extractor. Node-level extractor. Extracts `topics` metadata field.
    This was adapted from the `KeywordExtractor` class from `llama_index`.

    Args:
        llm (Optional[LLM]): LLM
        topics (int): number of topics to extract
        prompt_template (str): template for keyword extraction
    """

    llm: LLMPredictorType = Field(description="The LLM to use for generation.")
    topics: int = Field(default=5, description="The number of topics to extract.", gt=0)

    prompt_template: str = Field(
        default=DEFAULT_TOPIC_EXTRACT_TEMPLATE,
        description="Prompt template to use when generating topics.",
    )

    def __init__(
        self,
        llm: Optional[LLM] = None,
        # TODO: llm_predictor arg is deprecated
        llm_predictor: Optional[LLMPredictorType] = None,
        topics: int = 5,
        prompt_template: str = DEFAULT_TOPIC_EXTRACT_TEMPLATE,
        num_workers: int = DEFAULT_NUM_WORKERS,
        **kwargs: Any,
    ) -> None:
        """Init params."""
        if topics < 1:
            raise ValueError("num_topics must be >= 1")

        super().__init__(
            llm=llm or llm_predictor or Settings.llm,
            topics=topics,
            prompt_template=prompt_template,
            num_workers=num_workers,
            **kwargs,
        )

    @classmethod
    def class_name(cls) -> str:
        return "TopicExtractor"

    async def _aextract_topics_from_node(self, node: BaseNode) -> Dict[str, str]:
        """Extract topics from a node and return it's metadata dict."""
        if self.is_text_node_only and not isinstance(node, TextNode):
            return {}

        context_str = node.get_content(metadata_mode=self.metadata_mode)
        topics = await self.llm.apredict(
            PromptTemplate(template=self.prompt_template),
            topics=self.topics,
            context_str=context_str,
        )

        return {"topics": [topic.strip() for topic in topics.strip().split(",")]}

    async def aextract(self, nodes: Sequence[BaseNode]) -> List[Dict]:
        topics_jobs = []
        for node in nodes:
            topics_jobs.append(self._aextract_topics_from_node(node))

        metadata_list: List[Dict] = await run_jobs(
            topics_jobs, show_progress=self.show_progress, workers=self.num_workers
        )

        return metadata_list


class GeocodeLocationsTransformer(TransformComponent):

    geo_data_path: str = Field(description="Path to geo data CSV file.")
    df: pd.DataFrame = None

    def __init__(self, geo_data_path: str, *args, **kwargs) -> None:
        super().__init__(geo_data_path=geo_data_path, *args, **kwargs)

        self.geo_data_path = geo_data_path
        self.df = pd.read_csv(geo_data_path)

        self.df["Locality_name"] = self.df["Locality_name"].str.lower().str.strip()
        self.df["Associated_names"] = self.df["Associated_names"].fillna("")
        self.df["Associated_names"] = (
            self.df["Associated_names"].str.lower().str.strip()
        )

    def __call__(self, nodes, **kwargs) -> List[BaseNode]:
        for node in nodes:
            if "locations" in node.metadata:
                node.metadata["geo"] = self._geocode_locations(
                    node.metadata["locations"]
                )

        return nodes

    def _geocode_locations(self, locations: List[str]) -> Dict[str, List[float]]:
        geo = {}

        for location in locations:
            coords = self._geocode_location(location)
            if coords:
                geo[location] = coords

        return geo

    def _geocode_location(self, location: str) -> Optional[List[float]]:
        location = location.lower().strip()

        row = self.df[self.df["Locality_name"].str.lower() == location]

        if row.empty:
            row = self.df[self.df["Associated_names"].str.contains(location)]

        if not row.empty:
            row = row.iloc[0]

            if not np.isnan(row["Lat"]) and not np.isnan(row["Lon"]):
                return [row["Lat"], row["Lon"]]

        return None
