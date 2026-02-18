from typing import List
from src.schema.search import SearchResponse
from src.repository.user_repository import UserRepository
from src.repository.user_search_log_repository import UserSearchLogRepository

class SearchPipeline:
    def __init__(
        self,
        faiss_service,
        context_builder_service,
        search_service,
    ):
        self.faiss_service = faiss_service
        self.context_builder_service = context_builder_service
        self.search_service = search_service

        self.docs = []

    async def initialize_search_session(self, x: float, y: float) -> None:
        self.docs = await self.context_builder_service.build_search_context(x, y)
        await self.faiss_service.add_index(self.docs)
        self.search_service.prepare_search_context(self.docs)

    async def search_places(self, query: str) -> List[SearchResponse]:
        ranked_results = await self.search_service.HybridRetriever(query)

        url_map = {
            doc["restaurant"]: doc["place_url"]
            for doc in self.docs
        }

        return [
            SearchResponse(
                restaurant=name,
                place_url=url_map.get(name)
            ) for name, score in ranked_results
        ]
    
    def save_logs(self, ip_address: str, query: str) -> None:
        user_id = UserRepository.save(ip_address)
        UserSearchLogRepository.save(user_id, query)
    
    async def recommend(self, ip_address: str, x: float, y: float, query: str) -> List[SearchResponse]:
        self.save_logs(ip_address, query)
        await self.initialize_search_session(x, y)
        return await self.search_places(query)