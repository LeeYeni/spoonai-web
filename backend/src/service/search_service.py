from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document

from src.service.faiss_service import FAISSService

class SearchService:
    def __init__(self, faiss_service: FAISSService):
        self.dense_retriever = faiss_service
        self.sparse_retriever = None
        self.docs = []
        self.nearby_restaurants = []

    def prepare_search_context(self, docs: list):
        self.docs = [
            Document(
                page_content=doc["content"],
                metadata={
                    "restaurant": doc["restaurant"],
                    "place_url": doc["place_url"]
                }
            ) for doc in docs
        ]
        self.nearby_restaurants = [doc["restaurant"] for doc in docs]
        self.sparse_retriever = self.SparseRetriever()

    def SparseRetriever(self):
        """
        키워드를 기반으로 BM25 검색기를 생성합니다.
        """
        retriever = BM25Retriever.from_documents(self.docs)
        retriever.k = 20
        return retriever

    def rrf_score(self, sparse_results: list, dense_results: list, k: int = 20):
        """
        Reciprocal Rank Fusion 알고리즘입니다.
        score = 1 / (k + rank)
        """
        rrf_map = {}

        for rank, doc in enumerate(sparse_results, 1):
            name = doc.metadata.get("restaurant")
            rrf_map[name] = rrf_map.get(name, 0) + 1 / (k + rank)

        for rank, res in enumerate(dense_results, 1):
            name = res.get("restaurant")
            rrf_map[name] = rrf_map.get(name, 0) + 1 / (k + rank)

        sorted_rrf = sorted(rrf_map.items(), key=lambda x : x[1], reverse=True)
        return sorted_rrf

    async def HybridRetriever(self, query: str, top_k: int = 5):
        """
        Sparse + Dense 검색 후 RRF로 Reranking합니다.
        """
        sparse_results = await self.sparse_retriever.ainvoke(query)

        dense_results = await self.dense_retriever.search(query, self.nearby_restaurants)

        final_ranking = self.rrf_score(sparse_results, dense_results)

        return final_ranking[:top_k]