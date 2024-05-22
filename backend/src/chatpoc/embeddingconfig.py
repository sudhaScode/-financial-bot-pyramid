from langchain_community.embeddings import VertexAIEmbeddings
from utility.functionstore import rate_limit
from typing import List

class CustomVertexAIEmbeddings(VertexAIEmbeddings):
    requests_per_minute: int
    num_instances_per_batch: int
    index_type: str  # New attribute for indexing type (HNSW or IVF_FLAT)

    def __init__(self, requests_per_minute: int, num_instances_per_batch: int,
                 model_name: str, index_type: str = "IVF_FLAT"):
        super().__init__(model_name=model_name)  # Call base class constructor
        self.requests_per_minute = requests_per_minute
        self.num_instances_per_batch = num_instances_per_batch
        self.index_type = index_type.upper()  # Ensure case-insensitivity

    def embed_documents(self, texts: List[str]) -> List[List]:
        limiter = rate_limit(self.requests_per_minute)
        results = []
        docs = list(texts)

        while docs:
            head, docs = docs[:self.num_instances_per_batch], docs[self.num_instances_per_batch:]

            # Use Vertex AI indexing for efficient retrieval (if available)
            if self.index_type in ("HNSW", "IVF_FLAT"):
                embeddings = self.client.search(
                    query_embeddings=self.text_to_embeddings(head),
                    index_spec_name=self.model_name,  # Assuming model_name holds index name
                    # Additional indexing configuration might be needed here (e.g., ef for HNSW)
                )
                results.extend(embeddings)
            else:
                # Fallback to batch embedding generation (if indexing not supported)
                chunk = self.client.get_embeddings(head)
                results.extend(chunk)

            next(limiter)

        return [r.values for r in results]
