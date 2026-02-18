from fastapi import Request

from src.service.faiss_service import FAISSService
from src.service.context_builder_service import ContextBuilderService
from src.service.search_service import SearchService
from src.service.search_pipeline import SearchPipeline

faiss_service = FAISSService()
context_builder_service = ContextBuilderService(faiss_service)
search_service = SearchService(faiss_service)
search_pipeline = SearchPipeline(faiss_service, context_builder_service, search_service)

def get_faiss_service() -> FAISSService:
    return faiss_service

def get_context_builder_service() -> ContextBuilderService:
    return context_builder_service

def get_search_service() -> SearchService:
    return search_service

def get_search_pipeline() -> SearchPipeline:
    return search_pipeline

def get_client_ip(request: Request) -> str:
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]
    return request.client.host