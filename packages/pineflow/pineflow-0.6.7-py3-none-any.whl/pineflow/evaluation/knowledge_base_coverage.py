from typing import Dict, List

import numpy as np
from pydantic.v1 import BaseModel

from pineflow.core.embeddings import BaseEmbedding, SimilarityMode


class KnowledgeBaseCoverage(BaseModel):
    """Measures how much the knowledge base (context) has contributed to the answer’s coverage.
    Higher value suggests greater proportion of context are in LLM response.

    Args:
        embed_model (BaseEmbedding):
        similarity_mode (str, optional): Similarity strategy. Currently supports "cosine", "dot_product" and "euclidean". Defaults to ``cosine``.
        similarity_threshold (float, optional): Embedding similarity threshold for "passing". Defaults to ``0.8``.

     **Example**

    .. code-block:: python

        from pineflow.embeddings import HuggingFaceEmbedding
        from pineflow.evaluation import KnowledgeBaseCoverage

        embedding = HuggingFaceEmbedding()
        eval_coverage = KnowledgeBaseCoverage(embed_model=embedding)
    """

    embed_model: BaseEmbedding
    similarity_mode: SimilarityMode = SimilarityMode.COSINE
    similarity_threshold: float = 0.8

    class Config:
        arbitrary_types_allowed = True

    def compute_metric(self, contexts: List[str], candidate: str) -> Dict:
        """
        Args:
            contexts (List[str]): List text used as LLM context.
            candidate (str): LLM response based on given context.

        **Example**

        .. code-block:: python

            context_coverage = eval_coverage.compute_metric(context=[], candidate="<candidate>")
        """
        if not contexts or not candidate:
            raise ValueError("Must provide these parameters [`contexts`, `candidate`]")

        coverage = {"contexts_score": [], "score": 0}
        candidate_embedding = self.embed_model.get_query_embedding(candidate)

        for context in contexts:
            context_embedding = self.embed_model.get_query_embedding(context)
            coverage["contexts_score"].append(
                self.embed_model.similarity(candidate_embedding, context_embedding, mode=self.similarity_mode))

        coverage["score"] = np.mean(coverage["contexts_score"])
        coverage["passing"] = coverage["score"] >= self.similarity_threshold

        return coverage
